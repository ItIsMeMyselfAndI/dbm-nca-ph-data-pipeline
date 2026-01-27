-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.nca (
  id integer NOT NULL DEFAULT nextval('nca_id_seq'::regclass),
  release_id integer NOT NULL,
  nca_number text,
  nca_type text,
  agency text,
  department text,
  released_date date,
  purpose text,
  operating_unit ARRAY,
  amount ARRAY,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT nca_pkey PRIMARY KEY (id),
  CONSTRAINT fk_nca_release FOREIGN KEY (release_id) REFERENCES release(id)
);
CREATE TABLE public.release (
  id integer NOT NULL DEFAULT nextval('release_id_seq'::regclass),
  title text,
  filename text,
  url text,
  year integer,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT release_pkey PRIMARY KEY (id)
);
