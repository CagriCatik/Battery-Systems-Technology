# Guideline to Delete Deployments on GitHub

This guide will walk you through the steps to delete deployments on GitHub using the GitHub CLI (`gh`) or the repository settings.

---

## **Option 1: Manually Delete GitHub Pages Deployment via Repository Settings**
1. Navigate to your GitHub repository.
2. Click on the **Settings** tab.
3. Scroll down and click on **Pages** under the **Code and automation** section.
4. In the **GitHub Pages** section, click **Disable GitHub Pages** (if enabled). This action will stop GitHub Pages from serving your static site.
5. If you only want to delete the deployed files:
   - Switch to the **`gh-pages`** branch (or the branch used for Pages).
   - Delete the files or the entire branch.

---

## **Option 2: Delete Deployments Using GitHub CLI (`gh`)**
1. **Ensure GitHub CLI (`gh`) is installed** and configured:
   - Install from [GitHub CLI Installation Guide](https://cli.github.com/).
   - Run `gh auth login` to authenticate.

2. Retrieve a list of deployments:
   ```bash
   gh api /repos/<owner>/<repo>/deployments
   ```
   Replace `<owner>` and `<repo>` with your GitHub username and repository name (e.g., `CagriCatik/Battery-Systems-Technology`).

3. Find the **deployment ID** from the response. It will look like this:
   ```json
   [
     {
       "id": 123456789,
       "sha": "abc123...",
       "ref": "main",
       "task": "deploy"
     },
     ...
   ]
   ```

4. Use the deployment ID to delete the deployment:
   ```bash
   gh api -X DELETE /repos/<owner>/<repo>/deployments/<deployment_id>
   ```
   Example:
   ```bash
   gh api -X DELETE /repos/CagriCatik/Battery-Systems-Technology/deployments/123456789
   ```

5. If successful, you should see no error message. If the deployment still exists, double-check the ID and permissions.

---

## **Option 3: Automate with a Python Script**
If you prefer automation, you can use this Python script to delete deployments:

### Python Script:
```python
import requests

# Set your repo details and GitHub token
repo_owner = 'CagriCatik'
repo_name = 'Battery-Systems-Technology'
deployment_id = 'your-deployment-id'  # Replace with actual deployment ID
github_token = 'your-github-token'  # Replace with your personal access token

# API endpoint
url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/deployments/{deployment_id}'

# Headers for authentication
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Send DELETE request
response = requests.delete(url, headers=headers)

if response.status_code == 204:
    print('Deployment deleted successfully.')
else:
    print(f'Failed to delete deployment: {response.status_code}, {response.json()}')
```

---

## **Common Issues and Solutions**
- **404 Error ("Not Found")**: Ensure you are using the correct deployment ID and that your GitHub token has the necessary permissions.
- **Permission Issues**: Check that your account has write access to the repository and that your GitHub token includes the `repo` scope.
- **No Deployments Found**: Make sure you are checking the right branch and settings in your repository.

