# timectl



# timectl

<div align="center">

![timectl](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-%3E%3D%203.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)

a worklog for devs. Manage multiple projects with kubectl-like syntax. Simple and intuitive for developers.
</div>



## 🚀 Features

- **Kubernetes-inspired CLI**: Familiar syntax for developers who use kubectl
- **Project Management**: Create, list, describe, and delete projects
- **Issue Tracking**: Manage issues within projects with their own lifecycle
- **Time Logging**: Track time spent on specific issues
- **Statistics & Reports**: Get insights about your time allocation
- **Easy Configuration**: Simple config management like kubectl contexts

## 📋 Commands

### Project Management
```bash
# List all projects
timectl get projects

# Create a new project
timectl create project myproject

# Get detailed project information
timectl describe project myproject

# Delete a project
timectl delete project myproject
```

### Issue Management
```bash
# List issues in a project
timectl get issues -p myproject

# Create a new issue
timectl create issue -p myproject --name "auth-feature"

# Get detailed issue information
timectl describe issue auth-feature -p myproject
```

### Time Tracking
```bash
# Start tracking time on an issue
timectl start -p myproject -i auth-feature

# Add notes to current session
timectl note -p myproject -i auth-feature "Implementing OAuth flow"

# Stop tracking time
timectl stop -p myproject -i auth-feature

# List time entries
timectl get worklogs -p myproject -i auth-feature
```

### Statistics and Reports
```bash
# View project statistics
timectl get stats -p myproject

# Export time entries
timectl export worklogs -p myproject --format csv
```

## 📁 Project Structure

```
timectl/
├── cli/                      # CLI implementation
│   ├── cli.py               # Main CLI entry point
│   ├── commands/            # Command implementations
│   │   ├── config_commands.py    # Configuration management
│   │   ├── project_commands.py   # Project-related commands
│   │   ├── stats_commands.py     # Statistics and reporting
│   │   └── worklogs_commands.py  # Time tracking operations
├── docs/                    # Documentation
├── tests/                   # Test suite
│   ├── features/           # Behavior tests
│   │   ├── use-cases/     # Use case specifications
│   │   │   ├── config-management.feature
│   │   │   ├── describe-project.feature
│   │   │   ├── time-tracking.feature
│   │   │   └── ...
│   ├── test_project_cli.py      # CLI tests
│   └── test_project_functions.py # Function tests
├── pyproject.toml          # Project configuration
├── LICENSE
└── README.md
```

## 🔧 Installation

```bash
# Install from PyPI (coming soon)
pip install timectl

# Install from source
git clone https://github.com/yourusername/timectl.git
cd timectl
pip install -e .
```

## 💡 Use Cases

1. **Daily Development**
   ```bash
   # Start your day
   timectl start -p backend-api -i user-auth
   # Take a break
   timectl pause -p backend-api -i user-auth
   # Resume work
   timectl resume -p backend-api -i user-auth
   # End your day
   timectl stop -p backend-api -i user-auth
   ```

2. **Time Analysis**
   ```bash
   # View today's work
   timectl get stats -p backend-api --today
   # Export weekly report
   timectl export worklogs -p backend-api --week --format csv
   ```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific feature tests
pytest tests/features/use-cases/time-tracking.feature
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you encounter any problems or have suggestions:
1. Check the documentation in the `docs` folder
2. Search through [issues](link-to-issues)
3. Create a new issue if needed

---
Made with ❤️ for developers by CristianHZ