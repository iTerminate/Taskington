DROP TABLE IF EXISTS "role" CASCADE;
Create Table "role" (
	"id" SERIAL NOT NULL,
    "name" VARCHAR(30) NOT NULL,
    description VARCHAR(200),
    CONSTRAINT role_pkey PRIMARY KEY (Id),
    UNIQUE("name")
);

DROP TABLE IF EXISTS beamline CASCADE;
Create Table beamline (
	Id SERIAL NOT NULL,
    Name VARCHAR(30) NOT NULL,
    description VARCHAR(200),
    CONSTRAINT beamline_pkey PRIMARY KEY (Id),
    UNIQUE("name")
);

DROP TABLE IF EXISTS "user" CASCADE;
CREATE TABLE "user" (
    Id SERIAL NOT NULL,
    username VARCHAR(30) NOT NULL,
    local_password VARCHAR(30),
    CONSTRAINT user_pkey PRIMARY KEY (Id),
    UNIQUE(username)
);

DROP TABLE IF EXISTS user_beamline CASCADE;
CREATE TABLE user_beamline (
    beamline_id INTEGER REFERENCES beamline,
    user_id INTEGER REFERENCES "user" NOT NULL,
    UNIQUE (beamline_id, user_id)
);

DROP TABLE IF EXISTS user_role CASCADE;
CREATE TABLE user_role (
    user_id INTEGER REFERENCES "user" NOT NULL,
    role_id INTEGER REFERENCES "role" NOT NULL,
    UNIQUE (user_id, role_id)
);

DROP TABLE IF EXISTS software CASCADE;
CREATE TABLE software (
	id SERIAL NOT NULL,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(200),
    CONSTRAINT software_pkey PRIMARY KEY (Id),
    UNIQUE("name")
);

DROP TABLE IF EXISTS argument_type CASCADE;
CREATE TABLE argument_type (
	id SERIAL NOT NULL,
    type VARCHAR(20) NOT NULL,
    description VARCHAR(200),
    CONSTRAINT argument_type_pkey PRIMARY KEY (id),
    UNIQUE("type")
);

DROP TABLE IF EXISTS software_arg CASCADE;
CREATE TABLE software_arg (
    id SERIAL NOT NULL,
    software_id INTEGER REFERENCES software NOT NULL,
    key VARCHAR(25) NOT NULL,
    argument_type_id INTEGER REFERENCES argument_type NOT NULL,
    CONSTRAINT software_arg_pkey PRIMARY KEY (id),
    UNIQUE("software_id", "key")
);

DROP TABLE IF EXISTS process_node CASCADE;
CREATE TABLE process_node (
    id SERIAL NOT NULL,
    computer_name VARCHAR(32) NOT NULL,
    num_threads INT NOT NULL,
    hostname VARCHAR(32) NOT NULL,
    port INT NOT NULL,
    status VARCHAR(32) NOT NULL,
    heartbeat TIMESTAMP,
    process_cpu_percent FLOAT,
    process_mem_percent FLOAT,
    system_cpu_percent FLOAT,
    system_mem_percent FLOAT,
    system_swap_percent FLOAT,
    CONSTRAINT process_node_pkey PRIMARY KEY (id),
    UNIQUE("computer_name")
);

DROP TABLE IF EXISTS status CASCADE;
CREATE TABLE status (
	id SERIAL NOT NULL,
    status VARCHAR(20) NOT NULL,
    description VARCHAR(200),
    CONSTRAINT status_pkey PRIMARY KEY (id),
    UNIQUE("status")
);

DROP TABLE IF EXISTS job_status CASCADE;
CREATE TABLE job_status (
    id SERIAL NOT NULL,
    process_node_id INTEGER REFERENCES process_node NOT NULL,
    status_id INTEGER REFERENCES status NOT NULL,
    start_proc_time TIMESTAMP,
    finish_proc_time TIMESTAMP,
    log_path VARCHAR(100),
    CONSTRAINT job_status_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS job_dataset CASCADE;
CREATE TABLE job_dataset (
    id SERIAL NOT NULL,
    dataset_path varchar(100) NOT NULL,
    process_all bool NOT NULL,
    CONSTRAINT job_dataset_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS dataset_file_to_process CASCADE;
CREATE TABLE dataset_file_to_process (
    dataset_id INTEGER REFERENCES job_dataset NOT NULL,
    file_name VARCHAR(25) NOT NULL,
    UNIQUE (dataset_id, file_name)
);

DROP TABLE IF EXISTS job CASCADE;
CREATE TABLE job (
    id SERIAL NOT NULL,
    is_concurrent BOOLEAN NOT NULL,
    priority INTEGER NOT NULL,
    experiment_software_id INTEGER REFERENCES software NOT NULL,
    dataset_id INTEGER REFERENCES job_dataset NOT NULL,
    job_status_id INTEGER REFERENCES job_status NOT NULL,
    submitted_by_user_id INTEGER REFERENCES "user" NOT NULL,
    CONSTRAINT job_pkey PRIMARY KEY (id)
);

DROP TABLE IF EXISTS job_email CASCADE;
CREATE TABLE job_email (
    job_id INTEGER REFERENCES job NOT NULL,
    email VARCHAR(25) NOT NULL,
    attachment VARCHAR(25),
    UNIQUE (job_id, email)
);

DROP TABLE IF EXISTS job_software_arg CASCADE;
CREATE TABLE job_software_arg (
    job_id INTEGER REFERENCES job NOT NULL,
    software_args_id INTEGER REFERENCES software_arg NOT NULL,
    value VARCHAR(25),
    UNIQUE (job_id, software_args_id)
);

DROP TABLE IF EXISTS process_node_supported_software CASCADE;
CREATE TABLE process_node_supported_software (
    process_node_id INTEGER REFERENCES process_node NOT NULL,
    software_id INTEGER REFERENCES software NOT NULL,
    UNIQUE (process_node_id, software_id)
);