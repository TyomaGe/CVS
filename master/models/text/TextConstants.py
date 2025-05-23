MERGE_CONFLICT_TEXT = (
    "======== MERGE CONFLICT ========\n"
    "File: {conflict_file}\n"
    "Branch \"{merge_branch}\" has one version, while branch "
    "\"{target_branch}\" has another.\n\n"
    "What would you like to do?\n"
    "- Type \"{merge_branch}\" to accept the version from the "
    "\"{merge_branch}\" branch\n"
    "- Type \"{target_branch}\" to keep the version from your current "
    "branch \"{target_branch}\"\n"
    "- Type \"abort\" to cancel the merge process\n\n"
    "Your choice >> "
)

MERGE_ABORT_TEXT = (
    "\nMerge aborted.\n"
    "No changes have been made.\n"
    "You can resolve conflicts manually and try merging again later."
)

MERGE_COMMIT_TEXT = (
    "Merge branch '{merge_branch}' into '{target_branch}'"
)

MERGE_SUCCESS_TEXT = (
    "\033[36mMerge completed successfully!\033[0m\n"
    "Successfully merged branch '\033[1m{merge_branch}\033[0m' "
    "into '\033[1m{target_branch}\033[0m'\n"
    "Added {new_files_count} files, resolved {resolved_conflicts} conflicts"
)

ARGUMENT_PARSER_DESCRIPTION = (
    "CVS - a simple version control system\n"
    "Use this tool to manage your project files "
    "with commands like init, add, commit, "
    "status, log, reset, and etc"
)

ARGUMENT_PARSER_EPILOG = (
    "Examples:\n"
    "init\n"
    "add file.txt\n"
    "commit -m \"Commit message\"\n"
    "status"
)
