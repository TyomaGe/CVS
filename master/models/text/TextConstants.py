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
    "No changes have been made. You can resolve conflicts manually and\n"
    "try merging again later."
)

MERGE_COMMIT_TEXT = (
    "Merge branch '{merge_branch}' into {target_branch}"
)
