# Contributing guide  

## How to contribute?

Contributing to the project is very easy and every little bit counts! Just follow the following steps:

To contribute to this project, follow the next steps:

* *Fork* (just to external contributors)
* Create [*issues*](CONTRIBUTING.md##issues)
* Follow the commit policy [*commits*](CONTRIBUTING.md##commit-policy)
* Create [*branchs*](CONTRIBUTING.md##branches-policy)
* Submit [*Pull Request*](CONTRIBUTING.md##merges-and-pull-requests-policy)
* Tags and releases [*tags*](CONTRIBUTING.md##tags-and-releases-policy)

## Issues

Properly managing issues can help to keep track of the progress of a project, and make it easier for others to understand the current state of the project. This guide outlines the recommended issue policy for this project in a GitLab context.

### Types of issues

- **Bug**: A problem that causes the project to not work as intended.
- **Feature request**: A request for a new feature or improvement to the project.
- **Question**: A question about the project or its usage.

### Creating issues

- **Use a clear and descriptive title**: The title should summarize the issue in a few words and be specific enough to understand what the issue is about.
- **Use the appropriate label**: Label the issue with the appropriate label (e.g. "bug", "feature request", "question").
- **Provide a detailed description**: Include as much information as possible about the issue, including any relevant error messages, screenshots, and steps to reproduce the issue.
- **Include relevant information**: Include information about the environment (e.g. operating system, browser, version of the project) in which the issue occurred.
- **Use the template**: Use the template provided when creating the issue, to ensure all necessary information is included.
- **Assign the issue**: Assign the issue to the person who will be working on it, or leave it unassigned if it's not yet clear who will work on it.
- **Use milestones**: Use milestones to group issues that are related to a specific release or version of the project.

### Working on issues

- **Use the appropriate label**: Update the label to reflect the current status of the issue (e.g. "in progress", "waiting for feedback").
- **Provide regular updates**: Provide regular updates on the progress of the issue, and let others know if the issue is blocked or delayed.
- **Close the issue**: Close the issue when it's resolved, and include any relevant information (e.g. the version in which the bug was fixed) in the closing comment.
- **Reference the issue**: Reference the issue number in the commit message and merge request that resolves the issue, so that the issue is automatically closed when the merge request is merged.

## Commit Policy

Conventional Commits is a specification for adding human- and machine-readable meaning to commit messages. It provides an easy set of rules for creating an explicit commit history, making it easier to automatically generate changelogs and to understand the project history.

### Commit Message Format

Use the following commit message format: 

```bash
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type

The `<type>` must be one of the following:
- `fix`: for bug fixes
- `feat`: for new features
- `chore`: for changes to the build process or auxiliary tools and libraries
- `docs`: for documentation changes
- `style`: for changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: for code changes that neither fix a bug nor add a feature
- `perf`: for changes that improve performance
- `test`: for adding missing or correcting existing tests
- `build`: for changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- `ci`: for changes to CI configuration files and scripts
- `revert`: for commit that reverts a previous commit.

#### Scope

The `<scope>` is optional and should be a single word describing the affected area of the codebase (example scopes: user, item, cart)

#### Subject

The `<subject>` should be a short, imperative phrase describing the change. The first letter should be capitalized and do not end the subject line with a period

#### Body

The `<body>` should provide a more detailed explanation of the changes made in the commit. Use the body to explain the why and how of the changes, rather than the what.

#### Footer

The `<footer>`  optional and should be used to include additional information, such as issue numbers, breaking changes, or revert commits.

If the commit includes breaking changes, add the phrase `BREAKING CHANGE:` at the beginning of the footer, followed by a detailed explanation of the changes.
If the commit is a revert, include the revert: prefix in the footer, followed by the header of the commit being reverted.
If the commit is related to an issue, include the phrase `Issue: #<issue number>` in the footer.

#### Examples

Example of a commit message following this format:
  
  ```bash
feat(auth): Add login and logout functionality

The login and logout functionality now allows users to authenticate with their email and password.

Issue: #123
```

Example of a commit message with breaking changes:

```bash
feat(auth): Add login and logout functionality

The login and logout functionality now requires a new parameter in the API call. This may break existing clients that are not updated to use the new parameter.

BREAKING CHANGE: The API call for login and logout has been changed and now requires a new parameter.
```

Example of a revert commit message:
  
  ```bash
revert: feat(auth): Add login and logout functionality

This reverts commit abcdef123456.

```

#### Tooling

It's recommended to use tooling like commitlint, which can help you to lint your commit messages to ensure that they match the Conventional Commits format.

Other tools that can help you to follow this specification are [commitizen](https://pypi.org/project/commitizen/) this tool will help you to create a commit message following the Conventional Commits specification.

By following this guide and using Conventional Commits, you will be able to create a consistent and meaningful commit history that is easy to understand and use for automated tasks such as generating changelogs.

## Branches Policy

A well-defined branching strategy helps to keep the development process organized and efficient. This guide outlines the recommended branches policy for this project.

### Main branches

- `master`: This is the main branch where the source code of the project is always in a releasable state. Only release and merge commits should be made to this branch.
- `develop`: This is the branch where all development work is done. This branch should always contain the latest version of the code that is under development.

### Supporting branches

- `feature/*`: These branches are used for developing new features. Each feature should have its own branch, named `feature/<feature-name>`.
- `fix/*`: These branches are used for bug fixes. Each bug fix should have its own branch, named `fix/<fix-name>`.
- `hotfix/*`: These branches are used for quick fixes to the production code. Each hotfix should have its own branch, named `hotfix/<hotfix-name>`.

### Workflow

1. **Create a new feature branch**: When starting to work on a new feature, create a new branch named `feature/<feature-name>` from the `develop` branch.
2. **Commit your changes**: Work on the feature and commit your changes to the feature branch. Follow the Conventional Commits format for commit messages.
3. **Open a pull request**: When the feature is ready to be reviewed and merged, open a pull request from the feature branch to the `develop` branch.
4. **Review and merge**: Review the code changes, ask for feedback and make any necessary changes. Once the pull request is approved, merge the feature branch into `develop`.
5. **Delete the feature branch**: After the feature branch is merged, delete it from the repository.

6. **Create a new hotfix branch**: When a bug is found on the production code, create a new branch named `hotfix/<hotfix-name>` from the `master` branch.
7. **Commit your changes**: Work on the hotfix and commit your changes to the hotfix branch. Follow the Conventional Commits format for commit messages.
8. **Open a pull request**: When the hotfix is ready to be reviewed and merged, open a pull request from the hotfix branch to the `master` branch.
9. **Review and merge**: Review the code changes, ask for feedback and make any necessary changes. Once the pull request is approved, merge the hotfix branch into `master`.
10. **Delete the hotfix branch**: After the hotfix branch is merged, delete it from the repository.

11. **Create a new fix branch**: When a bug is found on the `develop` branch, create a new branch named `fix/<fix-name>` from the `develop` branch.
12. **Commit your changes**: Work on the fix and commit your changes to the fix branch. Follow the Conventional Commits format for commit messages.
13. **Open a pull request**: When the fix is ready to be reviewed and merged, open a pull request from the fix branch to the `develop` branch. 

## Merges and Pull Requests Policy

Properly managing merge requests and pull requests can help to keep the development process organized, and ensure that changes to the codebase are reviewed and tested before they are merged. This guide outlines the recommended merge and pull request policy for this project.

### Creating merge requests

- **Use a clear and descriptive title**: The title should summarize the changes in a few words and be specific enough to understand what the merge request is about.
- **Link to the issue**: If the merge request is related to an open issue, include a link to the issue in the description.
- **Provide a detailed description**: Include a detailed description of the changes, including any relevant information about the implementation or design decisions.
- **Include screenshots**: Include screenshots or GIFs, if applicable, to help illustrate the changes.
- **Use the template**: Use the template provided when creating the merge request, to ensure all necessary information is included.
- **Assign reviewers**: Assign one or more reviewers to the merge request, to ensure that it is reviewed by someone other than the person who created it.

### Reviewing merge requests

- **Check for completeness**: Check that the merge request includes all necessary information, including a detailed description of the changes, screenshots or GIFs, and links to related issues.
- **Test the changes**: Test the changes to ensure that they work as intended and don't introduce new bugs.
- **Check for style consistency**: Check that the changes follow the project's coding style and conventions.
- **Leave feedback**: Leave feedback on the merge request, including any suggestions for improvement or issues that need to be addressed.
- **Approve or request changes**: Approve the merge request or request changes, depending on whether the changes are ready to be merged or not.

### Merging merge requests

- **Check for approvals**: Check that the merge request has been reviewed and approved by the assigned reviewers.
- **Check for passing tests**: Check that all tests pass and that the build is passing before merging the request.
- **Check for conflicts**: Check for conflicts with other branches and resolve them before merging the request.
- **Use a descriptive commit message**: Use a descriptive commit message that summarizes the changes, and reference the merge request number.
- **Delete the branch**: Delete the branch after the merge request is merged.


## Tags and Releases Policy

Properly tagging releases can help to keep track of the different versions of a project, and make it easier to rollback to a previous version if necessary. This guide outlines the recommended tags policy for this project.

### Semantic Versioning

We use [Semantic Versioning](https://semver.org/) to version our releases. This means that the version number will have the format `MAJOR.MINOR.PATCH`, where:

- **MAJOR**: Incompatible changes are made to the API.
- **MINOR**: Backwards-compatible new features are added to the API.
- **PATCH**: Backwards-compatible bug fixes are made to the API.

### Tagging releases

- **Create a tag for every release**: Every time a new version of the project is released, create a new tag with the version number. The tag should be created from the `master` branch.
- **Use a consistent naming convention**: Use the format `vMAJOR.MINOR.PATCH` for the tag name. For example, `v1.0.0`.
- **Include release notes**: Include release notes in the tag message, describing the changes made in this release.

### Workflow

1. **Bump the version**: Update the version number in the project's `pyproject.toml` file, following the Semantic Versioning guidelines.
2. **Commit the version bump**: Commit the version bump to the `develop` branch, using the commit message format `chore(version): bump version to vMAJOR.MINOR.PATCH`.
3. **Create a release branch**: Create a new branch named `release/vMAJOR.MINOR.PATCH` from the `develop` branch.
4. **Merge release branch to master**: Merge the release branch to the `master` branch.
5. **Tag the release**: Create a tag from the `master` branch with the version number, following the format `vMAJOR.MINOR.PATCH`. Include release notes in the tag message.
6. **Merge master to develop**: Merge the `master` branch back to the `develop` branch.
7. **Delete the release branch**: After the release branch is merged, delete it from the repository.