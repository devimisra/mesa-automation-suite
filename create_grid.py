"""
create_grid.py
Generates MESA simulation directories based on a parameter grid.
"""
import itertools
import shutil
from pathlib import Path

def generate_grid(
    template_dir: Path, 
    runs_dir: Path, 
    m1_vals: list[float], 
    m2_vals: list[float], 
    porb_vals: list[float], 
    beta_ctrl: list[float]
) -> None:
    """Creates simulation directories and updates MESA inlist parameters."""
    runs_dir.mkdir(parents=True, exist_ok=True)
    joblist_path = Path('joblist.txt')

    with joblist_path.open('w', encoding='ascii') as f:
        job_id = 0
        for m1, m2, Porb, beta in itertools.product(m1_vals, m2_vals, porb_vals, beta_ctrl):
            job_id += 1
            run_name = f'm1-{m1:.1f}_m2-{m2:.1f}_Porb-{Porb:.3f}_b-{beta:.1f}'
            run_dir = runs_dir / run_name
            
            if run_dir.exists():
                shutil.rmtree(run_dir)
            shutil.copytree(template_dir, run_dir)

            # Edit inlist_project
            proj_file = run_dir / 'inlist_project'
            if proj_file.exists():
                lines = proj_file.read_text().splitlines()
                
                with proj_file.open('w') as pf:
                    for line in lines:
                        if 'm1 =' in line:
                            pf.write(f'   m1 = {m1}d0\n')
                        elif 'm2 =' in line:
                            pf.write(f'   m2 = {m2}d0\n')
                        elif 'initial_period_in_days' in line:
                            pf.write(f'   initial_period_in_days = {Porb}d0\n')
                        elif 'mass_transfer_beta =' in line:
                            pf.write(f'   mass_transfer_beta = {beta}d0\n')
                        else:
                            pf.write(line + '\n')
            
            f.write(f'{job_id} {run_name}\n')

    print(f'Prepared {job_id} runs. Mapping written to {joblist_path.name}')

if __name__ == "__main__":
    # Small toy grid for demonstration
    m1_vals = [1.4, 1.5]
    m2_vals = [1.0]
    porb_vals = [2.0, 3.0]
    beta_ctrl = [0.5]

    template_dir = Path("example_template")
    runs_dir = Path("toy_runs")

    generate_grid(template_dir, runs_dir, m1_vals, m2_vals, porb_vals, beta_ctrl)