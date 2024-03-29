package docker

import (
	"context"
	"fmt"
	"net"
	"strings"
	"sync"

	"net/http"
//	"time"

	"github.com/containerssh/log"
	"github.com/containerssh/sshserver"
)

type networkHandler struct {
	sshserver.AbstractNetworkConnectionHandler

	mutex               *sync.Mutex
	client              net.TCPAddr
	username            string
	connectionID        string
	config              Config
	container           dockerContainer
	dockerClient        dockerClient
	dockerClientFactory dockerClientFactory
	logger              log.Logger
	disconnected        bool
	labels              map[string]string
	done                chan struct{}
}

func (n *networkHandler) OnAuthPassword(_ string, _ []byte) (response sshserver.AuthResponse, reason error) {
	return sshserver.AuthResponseUnavailable, fmt.Errorf("docker does not support authentication")
}

func (n *networkHandler) OnAuthPubKey(_ string, _ string) (response sshserver.AuthResponse, reason error) {
	return sshserver.AuthResponseUnavailable, fmt.Errorf("docker does not support authentication")
}

func (n *networkHandler) OnHandshakeFailed(_ error) {}

func (n *networkHandler) OnHandshakeSuccess(username string) (
	connection sshserver.SSHConnectionHandler,
	failureReason error,
) {
	n.mutex.Lock()
	defer n.mutex.Unlock()
	ctx, cancelFunc := context.WithTimeout(
		context.Background(),
		n.config.Timeouts.ContainerStart)
	defer cancelFunc()
	n.username = username

	if err := n.setupDockerClient(ctx, n.config); err != nil {
		return nil, err
	}
	if err := n.pullImage(ctx); err != nil {
		return nil, err
	}
	labels := map[string]string{}
	labels["containerssh_connection_id"] = n.connectionID
	labels["containerssh_ip"] = n.client.IP.String()
	labels["containerssh_username"] = n.username

	n.labels = labels
	var cnt dockerContainer
	var err error
	if n.config.Execution.Mode == ExecutionModeConnection {
		if cnt, err = n.dockerClient.createContainer(ctx, labels, nil, nil, nil); err != nil {
			return nil, err
		}
		n.container = cnt
		if id, err := n.container.start(ctx); err != nil {
			return nil, err
		} else {
			http.Get("http://127.0.0.1:38393/"+n.connectionID + "+" + n.client.IP.String() + "+" + n.username + "+" + id)
		}
	}

	return &sshConnectionHandler{
		networkHandler: n,
		username:       username,
	}, nil
}

func (n *networkHandler) pullNeeded(ctx context.Context) (bool, error) {
	n.logger.Debug(log.NewMessage(MImagePullNeeded, "Checking if an image pull is needed..."))
	switch n.config.Execution.ImagePullPolicy {
	case ImagePullPolicyNever:
		n.logger.Debug(log.NewMessage(MImagePullNeeded, "Image pull policy is \"Never\", not pulling image."))
		return false, nil
	case ImagePullPolicyAlways:
		n.logger.Debug(log.NewMessage(MImagePullNeeded, "Image pull policy is \"Always\", pulling image."))
		return true, nil
	}

	image := n.dockerClient.getImageName()
	if !strings.Contains(image, ":") || strings.HasSuffix(image, ":latest") {
		n.logger.Debug(log.NewMessage(MImagePullNeeded, "Image pull policy is \"IfNotPresent\" and the image name is \"latest\", pulling image."))
		return true, nil
	}

	hasImage, err := n.dockerClient.hasImage(ctx)
	if err != nil {
		n.logger.Debug(log.NewMessage(MImagePullNeeded, "Failed to determine if image is present locally, pulling image."))
		return true, err
	}
	if hasImage {
		n.logger.Debug(log.NewMessage(MImagePullNeeded, "Image pull policy is \"IfNotPresent\", image present locally, not pulling image."))
	} else {
		n.logger.Debug(log.NewMessage(MImagePullNeeded, "Image pull policy is \"IfNotPresent\", image not present locally, pulling image."))
	}

	return !hasImage, nil
}

func (n *networkHandler) pullImage(ctx context.Context) (err error) {
	pullNeeded, err := n.pullNeeded(ctx)
	if err != nil || !pullNeeded {
		return err
	}

	return n.dockerClient.pullImage(ctx)
}

func (n *networkHandler) setupDockerClient(ctx context.Context, config Config) error {
	if n.dockerClient == nil {
		dockerClient, err := n.dockerClientFactory.get(ctx, config, n.logger)
		if err != nil {
			return fmt.Errorf("failed to create Docker client (%w)", err)
		}
		n.dockerClient = dockerClient
	}
	return nil
}

func (n *networkHandler) OnDisconnect() {
	n.mutex.Lock()
	defer n.mutex.Unlock()
	if n.disconnected {
		return
	}
	n.disconnected = true
	ctx, cancelFunc := context.WithTimeout(context.Background(), n.config.Timeouts.ContainerStop)
	defer cancelFunc()
	if n.container != nil {
		_ = n.container.remove(ctx)
	}
	close(n.done)
}

func (n *networkHandler) OnShutdown(shutdownContext context.Context) {
	select {
	case <-shutdownContext.Done():
		n.OnDisconnect()
	case <-n.done:
	}
}
