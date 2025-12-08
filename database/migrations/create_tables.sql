\connect lm4smells_db;

-- Table with LMs-based classification codes
BEGIN;
CREATE TABLE IF NOT EXISTS code_smells_v1 (
    task_id TEXT NOT NULL DEFAULT 'nd',
    smell_type TEXT NOT NULL DEFAULT 'nd', 
    explanation TEXT NOT NULL DEFAULT 'nd',
    file_name TEXT NOT NULL,
    model TEXT NOT NULL,
    programming_language TEXT NOT NULL,
    class_name TEXT,
    method_name TEXT,
    analyse_type TEXT NOT NULL DEFAULT 'nd',
    code TEXT NOT NULL,
    prompt_type TEXT NOT NULL DEFAULT 'nd',
    prompt TEXT NOT NULL,
    is_composite_prompt BOOLEAN NOT NULL,
    code_metric TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMIT;


-- Table with AST-based classification codes
BEGIN;
CREATE TABLE IF NOT EXISTS ast_codes (
    id TEXT NOT NULL DEFAULT 'nd',
    smell_type TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    metrics TEXT NOT NULL,
    definition_author TEXT NOT NULL,
    threshold_used INTEGER DEFAULT NULL,
    detected_at TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMIT;

-- Table with DL-based classification codes
BEGIN;
CREATE TABLE IF NOT EXISTS dl_codes (
    id TEXT NOT NULL DEFAULT 'nd',
    file_name TEXT NOT NULL,
    classification TEXT NOT NULL,
    model_used TEXT NOT NULL,
    element_name TEXT,
    element_type TEXT,
    confidence_score REAL,
    metrics TEXT,
    raw_code TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMIT;

-- Table with ML-based classification codes
BEGIN;
CREATE TABLE IF NOT EXISTS ml_codes (
    id TEXT NOT NULL DEFAULT 'nd',
    file_name TEXT NOT NULL,
    classification TEXT NOT NULL,
    model_used TEXT NOT NULL,
    element_name TEXT,
    element_type TEXT,
    confidence_score REAL,
    metrics TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMIT;

-- Table to manage tasks
BEGIN;
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    task_type TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMIT;