#!/bin/bash

# Example script showing how to generate vignettes
# Make sure to add your OpenAI API key to .env first!

echo "=== Vignette Generator Examples ==="
echo ""
echo "Before running, make sure to:"
echo "1. Add your OpenAI API key to .env file"
echo "2. Run: npm install"
echo ""
echo "Usage examples:"
echo ""

echo "Example 1: Generate page 3 (Database course with AI assistance)"
echo "node generate-vignette.js \\"
echo "  'A third-year database systems course' \\"
echo "  'Students were asked to design a normalized relational database schema' \\"
echo "  'Student used ChatGPT to generate initial ER diagram, then manually refined it to 3NF' \\"
echo "  3"
echo ""

echo "Example 2: Generate page 4 (No AI assistance)"
echo "node generate-vignette.js \\"
echo "  'A second-year data structures course' \\"
echo "  'Implement a balanced AVL tree from scratch' \\"
echo "  'Student manually coded all methods without AI, using paper diagrams for understanding' \\"
echo "  4"
echo ""

echo "Example 3: Run with default example"
echo "node generate-vignette.js"
echo ""

echo "To actually generate a page, uncomment one of the commands below:"
echo ""

# Uncomment to run:
# node generate-vignette.js \
#   "A third-year database systems course" \
#   "Students were asked to design a normalized relational database schema for an e-commerce platform" \
#   "In a third-year database course, a student was assigned to design a normalized database schema for an e-commerce system. The student used ChatGPT to generate an initial set of tables and relationships based on their requirements document. The AI produced a complete ER diagram with entities for Users, Products, Orders, and Reviews, including primary keys, foreign keys, and cardinality. The student then manually reviewed the schema, identified normalization issues, and refined the design to reach 3NF." \
#   3
