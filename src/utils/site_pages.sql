-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable the uuid-ossp extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the site_pages table for storing search results and company data
CREATE TABLE IF NOT EXISTS site_pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    url TEXT,
    chunk_number INTEGER,
    title TEXT,
    summary TEXT,
    content TEXT,
    company_name TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);

-- Create an index for faster vector similarity search
CREATE INDEX IF NOT EXISTS site_pages_embedding_idx ON site_pages USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Create a function for similarity search
CREATE OR REPLACE FUNCTION match_site_pages(query_embedding VECTOR(1536), match_threshold FLOAT, match_count INT)
RETURNS TABLE(
    id UUID,
    url TEXT,
    chunk_number INTEGER,
    title TEXT,
    summary TEXT,
    content TEXT,
    company_name TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        site_pages.id,
        site_pages.url,
        site_pages.chunk_number,
        site_pages.title,
        site_pages.summary,
        site_pages.content,
        site_pages.company_name,
        site_pages.metadata,
        1 - (site_pages.embedding <=> query_embedding) AS similarity
    FROM site_pages
    WHERE 1 - (site_pages.embedding <=> query_embedding) > match_threshold
    ORDER BY similarity DESC
    LIMIT match_count;
END;
$$; 