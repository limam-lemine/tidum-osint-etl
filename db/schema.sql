CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- domain table
CREATE TABLE domain (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),  
    classification TEXT,
    CONSTRAINT classification_valid_values
        CHECK (classification IS NULL OR classification IN ('malicious', 'suspicious', 'benign'))
);

-- job table tracks each scan run for a domain
CREATE TABLE job (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain_id UUID NOT NULL REFERENCES domain(id),
    status TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),   
    finished_at TIMESTAMPTZ                           
);

-- DNS records
CREATE TABLE dns_records (
    dns_id SERIAL PRIMARY KEY,
    domain_id UUID NOT NULL REFERENCES domain(id),
    a TEXT[],
    aaaa TEXT[],
    ns TEXT[],
    mx TEXT[],
    cname TEXT[],
    txt TEXT[]  
);

-- whois lookup
CREATE TABLE whois_lookup (
    whois_id SERIAL PRIMARY KEY,
    domain_id UUID NOT NULL REFERENCES domain(id),
    registrar TEXT,
    registrar_url TEXT,
    reseller TEXT,
    whois_server TEXT,
    referral_url TEXT,
    updated_date TIMESTAMPTZ,
    creation_date TIMESTAMPTZ,
    expiration_date TIMESTAMPTZ,
    name_servers TEXT[],
    status TEXT[],
    emails TEXT[],
    dnssec TEXT,
    name TEXT,
    org TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    registrant_postal_code TEXT,
    country TEXT,
    tech_name TEXT,
    tech_org TEXT,
    admin_name TEXT,
    admin_org TEXT
);

-- HTTP metadata
CREATE TABLE http_metadata (
    http_id SERIAL PRIMARY KEY,
    domain_id UUID NOT NULL REFERENCES domain(id),
    location TEXT,
    content_type TEXT,
    content_security_policy_report_only TEXT,
    response_date TIMESTAMPTZ, 
    expires TEXT,
    cache_control TEXT,
    server TEXT,
    content_length TEXT,
    x_xss_protection TEXT,
    x_frame_options TEXT,
    alt_svc TEXT,
    final_url TEXT,
    nbr_redirection INTEGER
);