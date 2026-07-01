-- Migration 002: review_stage column for input-required events
-- Enables Reviewer to know WHICH milestone step to review.

ALTER TABLE a2a_tasks ADD COLUMN review_stage TEXT;
-- Values: b1, b2, dev, red, test, gate, audit
