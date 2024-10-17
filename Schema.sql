CREATE TABLE Rules (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,  -- Ensures rule names are unique
  description TEXT,
  rule_expression TEXT NOT NULL  -- Ensure that rule expressions are always provided
);

CREATE TABLE RuleConditions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  rule_id INT NOT NULL,  -- Ensure rule_id is not null
  attribute VARCHAR(255) NOT NULL,  -- Ensure attribute is provided
  operator VARCHAR(255) NOT NULL,     -- Ensure operator is provided
  value VARCHAR(255) NOT NULL,         -- Ensure value is provided
  FOREIGN KEY (rule_id) REFERENCES Rules(id) ON DELETE CASCADE  -- Added ON DELETE CASCADE for referential integrity
);

CREATE TABLE RuleCombinations (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,  -- Ensures unique names for combinations
  description TEXT,
  combined_rule_expression TEXT NOT NULL  -- Ensure combined rule expressions are always provided
);
