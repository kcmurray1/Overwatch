export interface VolumeBinding {
  bind: string;
  mode: "rw" | "ro";
}

export interface RestartPolicy {
  Name: "always" | "unless-stopped" | "on-failure" | "no";
}

export interface ContainerSpec {
  name: string;
  image: string;
  detach?: boolean;
  user?: string;
  shm_size?: string;
  restart_policy?: RestartPolicy;
  ports?: Record<string, number | string>;
  volumes?: Record<string, VolumeBinding | string>;
  environment?: Record<string, any>;
  
  // Index signature: Allows any extra Docker SDK parameters (e.g., privileged, network_mode, labels)
  [key: string]: any;
}

export interface ContainerConfig {
  id: number;
  name: string;
  description?: string | null;
  spec: ContainerSpec;
  created_at: string;
  updated_at: string;
  machine_ids: number[];
}