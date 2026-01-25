CREATE TABLE release (
    id SERIAL PRIMARY KEY,
    title TEXT,
    url TEXT,
    year INTEGER,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE nca (
    id SERIAL PRIMARY KEY,
    release_id INTEGER NOT NULL,
    nca_number TEXT,
    nca_type TEXT,
    agency TEXT,
    department TEXT,
    released_date DATE,
    operating_unit TEXT,
    amount DECIMAL(15, 2),
    purpose TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_nca_release
        FOREIGN KEY (release_id)
        REFERENCES release(id)
        ON DELETE CASCADE,

    UNIQUE(nca_number)
)
