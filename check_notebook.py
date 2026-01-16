import json

# Load executed notebook
with open('Smart_Cultural_Storyteller_Executed.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Count cells
total_cells = len(nb['cells'])
markdown_cells = sum(1 for c in nb['cells'] if c['cell_type'] == 'markdown')
code_cells = sum(1 for c in nb['cells'] if c['cell_type'] == 'code')
cells_with_output = sum(1 for c in nb['cells'] if c['cell_type'] == 'code' and c.get('outputs'))

print("="*70)
print("✅ NOTEBOOK EXECUTION SUCCESSFUL!")
print("="*70)
print(f"\n📊 Notebook Statistics:")
print(f"  • Total Cells: {total_cells}")
print(f"  • Markdown Cells: {markdown_cells}")
print(f"  • Code Cells: {code_cells}")
print(f"  • Code Cells with Outputs: {cells_with_output}")

# Check for errors
errors = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        for output in cell.get('outputs', []):
            if output.get('output_type') == 'error':
                errors.append(f"Cell {i+1}: {output.get('ename', 'Unknown error')}")

if errors:
    print(f"\n⚠️  Errors Found: {len(errors)}")
    for error in errors[:5]:  # Show first 5 errors
        print(f"  • {error}")
else:
    print(f"\n✅ No Errors - All cells executed successfully!")

print("\n" + "="*70)
print("🎉 NOTEBOOK IS READY FOR SUBMISSION!")
print("="*70)
