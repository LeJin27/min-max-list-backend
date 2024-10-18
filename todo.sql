CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,         -- Unique ID for each task
    title VARCHAR(255) NOT NULL,   -- Task title
    description TEXT,              -- Task description (optional)
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- Task status: pending, in-progress, or completed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when task was created
    due_date TIMESTAMP             -- Optional due date for the task
);

INSERT INTO tasks (title, description, status, due_date)
VALUES 
('Finish Project', 'Complete the final project for school', 'pending', '2024-10-20'),
('Buy Groceries', 'Get milk, bread, and eggs', 'pending', '2024-10-15');
