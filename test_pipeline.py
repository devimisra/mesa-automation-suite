"""
test_pipeline.py
Unit tests for the MESA grid orchestration pipeline.
"""
from pathlib import Path
from create_grid import generate_grid

def test_generate_grid_creates_directories(tmp_path: Path):
    """Tests if the grid generator correctly duplicates templates and creates mapping."""
    # Setup mock template in the temporary test directory
    template_dir = tmp_path / "example_template"
    template_dir.mkdir()
    
    inlist_proj = template_dir / "inlist_project"
    inlist_proj.write_text("&binary_controls\n   m1 = 1.0d0\n   m2 = 1.4d0\n/ ! end")
    
    runs_dir = tmp_path / "toy_runs"
    
    # Define test grid
    m1_vals = [1.4, 1.5]
    m2_vals = [1.0]
    porb_vals = [2.0]
    beta_ctrl = [0.5]
    
    # Execute
    generate_grid(template_dir, runs_dir, m1_vals, m2_vals, porb_vals, beta_ctrl)
    
    # Assertions
    joblist = Path("joblist.txt")
    assert joblist.exists(), "joblist.txt was not created"
    
    lines = joblist.read_text().splitlines()
    assert len(lines) == 2, "joblist.txt should contain exactly 2 run mappings"
    
    run1_dir = runs_dir / "m1-1.4_m2-1.0_Porb-2.000_b-0.5"
    run2_dir = runs_dir / "m1-1.5_m2-1.0_Porb-2.000_b-0.5"
    
    assert run1_dir.exists()
    assert run2_dir.exists()
    
    # Verify parameter injection
    run1_inlist = run1_dir / "inlist_project"
    content = run1_inlist.read_text()
    assert "m1 = 1.4d0" in content
    
    # Cleanup
    joblist.unlink()