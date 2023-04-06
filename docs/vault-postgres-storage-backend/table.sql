-- Grant `vault_db` database permission to `vault` user
GRANT CONNECT ON DATABASE vault_db to vault;
GRANT ALL ON SCHEMA public TO vault WITH GRANT OPTION;

-- Vault storage backend schema and indexes
CREATE TABLE vault_kv_store (
  parent_path TEXT COLLATE "C" NOT NULL,
  path        TEXT COLLATE "C",
  key         TEXT COLLATE "C",
  value       BYTEA,
  CONSTRAINT pkey PRIMARY KEY (path, key)
);

CREATE INDEX parent_path_idx ON vault_kv_store (parent_path);

-- Store for HAEnabled backend
CREATE TABLE vault_ha_locks (
  ha_key                                      TEXT COLLATE "C" NOT NULL,
  ha_identity                                 TEXT COLLATE "C" NOT NULL,
  ha_value                                    TEXT COLLATE "C",
  valid_until                                 TIMESTAMP WITH TIME ZONE NOT NULL,
  CONSTRAINT ha_key PRIMARY KEY (ha_key)
);

-- Grant `vault_kv_store` and `vault_ha_locks table` permissions to `vault` user
GRANT ALL PRIVILEGES ON TABLE vault_kv_store TO vault;
GRANT ALL PRIVILEGES ON TABLE vault_ha_locks TO vault;
-- GRANT USAGE, SELECT ON SEQUENCE vault_kv_store_id_seq TO vault;

