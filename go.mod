module github.com/containerssh/docker

go 1.14

require (
	github.com/Microsoft/go-winio v0.4.16 // indirect
	github.com/containerd/containerd v1.4.4 // indirect
	github.com/containerssh/geoip v1.0.0
	github.com/containerssh/log v1.0.0
	github.com/containerssh/metrics v1.0.0
	github.com/containerssh/sshserver v1.0.0
	github.com/containerssh/structutils v1.0.0
	github.com/containerssh/unixutils v1.0.0
	github.com/docker/distribution v2.7.1+incompatible
	github.com/docker/docker v20.10.5+incompatible
	github.com/docker/go-connections v0.4.0 // indirect
	github.com/docker/go-units v0.4.0 // indirect
	github.com/gogo/protobuf v1.3.2 // indirect
	github.com/golang/protobuf v1.5.2 // indirect
	github.com/google/go-cmp v0.5.5
	github.com/gorilla/mux v1.8.0 // indirect
	github.com/moby/term v0.0.0-20201216013528-df9cb8a40635 // indirect
	github.com/morikuni/aec v1.0.0 // indirect
	github.com/opencontainers/go-digest v1.0.0 // indirect
	github.com/opencontainers/image-spec v1.0.1
	github.com/sirupsen/logrus v1.8.1 // indirect
	github.com/stretchr/testify v1.7.0
	golang.org/x/crypto v0.0.0-20210220033148-5ea612d1eb83 // indirect
	golang.org/x/net v0.0.0-20210331212208-0fccb6fa2b5c // indirect
	golang.org/x/time v0.0.0-20210220033141-f8bda1e9f3ba // indirect
	google.golang.org/genproto v0.0.0-20210401141331-865547bb08e2 // indirect
	gopkg.in/yaml.v3 v3.0.0-20210107192922-496545a6307b
	gotest.tools/v3 v3.0.3 // indirect
)

// Fixes CVE-2020-9283
replace (
	golang.org/x/crypto v0.0.0-20190308221718-c2843e01d9a2 => golang.org/x/crypto v0.0.0-20210220033148-5ea612d1eb83
	golang.org/x/crypto v0.0.0-20191011191535-87dc89f01550 => golang.org/x/crypto v0.0.0-20210220033148-5ea612d1eb83
	golang.org/x/crypto v0.0.0-20200220183623-bac4c82f6975 => golang.org/x/crypto v0.0.0-20210220033148-5ea612d1eb83
	golang.org/x/crypto v0.0.0-20200622213623-75b288015ac9 => golang.org/x/crypto v0.0.0-20210220033148-5ea612d1eb83
)

// Fixes CVE-2020-14040
replace (
	golang.org/x/text v0.3.0 => golang.org/x/text v0.3.3
	golang.org/x/text v0.3.1 => golang.org/x/text v0.3.3
	golang.org/x/text v0.3.2 => golang.org/x/text v0.3.3
)

// Fixes CVE-2019-11254
replace (
	gopkg.in/yaml.v2 v2.2.0 => gopkg.in/yaml.v2 v2.2.8
	gopkg.in/yaml.v2 v2.2.1 => gopkg.in/yaml.v2 v2.2.8
	gopkg.in/yaml.v2 v2.2.2 => gopkg.in/yaml.v2 v2.2.8
	gopkg.in/yaml.v2 v2.2.3 => gopkg.in/yaml.v2 v2.2.8
	gopkg.in/yaml.v2 v2.2.4 => gopkg.in/yaml.v2 v2.2.8
	gopkg.in/yaml.v2 v2.2.5 => gopkg.in/yaml.v2 v2.2.8
	gopkg.in/yaml.v2 v2.2.6 => gopkg.in/yaml.v2 v2.2.8
	gopkg.in/yaml.v2 v2.2.7 => gopkg.in/yaml.v2 v2.2.8
)
