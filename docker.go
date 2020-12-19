package docker

import (
	"context"
	"io"

	"github.com/containerssh/log"
)

// dockerClientFactory creates a dockerClient based on a configuration
type dockerClientFactory interface {
	// get takes a configuration and returns a docker client if the configuration was populated.
	// Returns an error if the configuration is invalid. Returns errDockerClientNotConfigured if the specific client is
	// not configured
	get(ctx context.Context, config Config, logger log.Logger) (dockerClient, error)
}

// dockerClient is a simplified representation of a docker client.
type dockerClient interface {
	// getImageName returns the configured image name
	getImageName() string

	// hasImage checks if the the configured image exists on the Docker daemon. Returns true if yes, false if no, and an
	// error if an error happened while querying the Docker daemon.
	hasImage(ctx context.Context) (bool, error)

	// pullImage pulls the configured image within the specified ctx and returns an error if the pull failed.
	pullImage(ctx context.Context) error

	// createContainer creates and starts the configured container. May return a container even if an error happened.
	// This container will need to be removed. Passing tty also means that the main console will be prepared for
	// attaching.
	createContainer(
		ctx context.Context,
		labels map[string]string,
		env map[string]string,
		tty *bool,
		cmd []string,
	) (dockerContainer, error)
}

// dockerContainer is the representation of a created container.
type dockerContainer interface {
	// attach attaches to the container on the main console.
	attach(ctx context.Context) (dockerExecution, error)

	// start starts the container within the given context.
	start(ctx context.Context) error

	// createExec creates an execution process for the given program with the given parameters. The passed context is
	// the start context.
	createExec(ctx context.Context, program []string, env map[string]string, tty bool) (dockerExecution, error)

	// remove removes the container within the given context.
	remove(ctx context.Context) error
}

// dockerExecution is an execution process on either an "exec" process or attached to the main console of a container.
type dockerExecution interface {
	resize(ctx context.Context, height uint, width uint) error
	run(
		stdout io.Writer,
		stderr io.Writer,
		stdin io.Reader,
		onExit func(exitStatus int),
	)
}