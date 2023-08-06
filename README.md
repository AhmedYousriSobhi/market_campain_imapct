# Data Scientist Evaluation Task
| Info | Description |
|:-----:|:----------:|
| Project Objective | Market Campain Performance Analysis on Sport Company |
| Assignee | Ahmed Yousri Sobhi |
| Assignee's email | [ahmedyousrisobhi@gmail.com](ahmedyousrisobhi@gmail.com) |

## Project Structure
```bash
.
├── data                   # Dataset files
|   ├── raw
|   ├── intermid
|   ├── output
├── nb_workspace           # Jupiter notebooks
├── docs                   # Documentation files which includes analysis report
├── report                 # Reports files
|   ├── plots              # Figures files
|   ├── reports            # Reports HTML files
├── src                    # Source scripts files
|   ├── env                # Script file to create project directory environment
|   ├── model              # Exported trained models
└── README.md
```
## Setup Environment
Go inside the project directory
```
cd project_directory
```
Install Required Libararies and packages.
```
pip install -r requirements.txt
```

In case of initial setup, create required folders directory using environment script
```
python ./src/env/setup_env.py
```
## Analysis Report
Included inside directory -> docs/analysis_report.pdf