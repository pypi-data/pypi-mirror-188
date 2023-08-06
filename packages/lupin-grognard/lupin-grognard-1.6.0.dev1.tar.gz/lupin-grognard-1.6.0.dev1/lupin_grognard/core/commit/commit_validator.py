import re

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.commit.commit_reporter import CommitReporter
from lupin_grognard.core.commit.commit_error import ErrorCount
from lupin_grognard.core.config import (
    INITIAL_COMMIT,
    EMOJI_CHECK,
    EMOJI_CROSS,
    PATTERN,
)


class CommitValidator(Commit):
    def __init__(self, commit: str, error: ErrorCount):
        super().__init__(commit=commit)
        self.reporter = CommitReporter(commit)
        self.error = error

    def perform_checks(self, merge_option: bool) -> None:
        if merge_option:  # check merge commits have approvers
            if self._is_merge_commit(self.title):
                if not self._validate_commit_merge():
                    self.error.increment_merge_error()
            else:
                if not self._validate_commit_title():
                    self.error.increment_title_error()
                if not self._validate_commit_body():
                    self.error.increment_body_error()
        else:
            if not self._validate_commit_title():
                self.error.increment_title_error()
            if not self._is_merge_commit(self.title):
                if not self._validate_commit_body():
                    self.error.increment_body_error()

    def _validate_commit_title(self) -> bool:
        if self._validate_commit_message(self.title):
            self.reporter.display_title_report(EMOJI_CHECK)
            return True
        else:
            self.reporter.display_title_report(EMOJI_CROSS)
            return False

    def _validate_commit_body(self) -> bool:
        if self.body:
            message_error = []
            for message in self.body:
                if self._validate_commit_message(message):
                    message_error.append(message)
            if len(message_error) > 0:
                self.reporter.display_body_report(message_error)
                return False  # must not start with a conventional message
        return True

    def _validate_commit_message(self, commit_msg: str, pattern: str = PATTERN):
        if self._is_special_commit(commit_msg):
            return True

        match = re.match(pattern, commit_msg)
        if match:
            if self._is_feat_commit(match):
                return self._validate_commit_message_for_feat_type(match)
            else:
                return self._validate_commit_message_for_generic_type(match)
        else:
            return False

    def _is_special_commit(self, commit_msg: str) -> bool:
        return (
            commit_msg.startswith(("Merge", "Revert", "fixup!", "squash!"))
            or commit_msg in INITIAL_COMMIT
        )

    def _is_merge_commit(self, commit_msg: str) -> bool:
        return commit_msg.startswith("Merge")

    def _validate_commit_merge(self) -> bool:
        self.reporter.display_merge_report(approvers=self.approvers)
        if len(self.approvers) < 1:
            return False
        return True

    def _is_feat_commit(self, match) -> bool:
        type, _, *_ = match.groups()
        return type == "feat"

    def _validate_commit_message_for_feat_type(self, match: str) -> bool:
        """Validates a commit type 'feat' contains a scope of one of the following: add, change, remove"""
        _, scope, *_ = match.groups()
        if scope is None or scope not in ["(add)", "(change)", "(remove)"]:
            self.error.increment_feat_scope_error()
            return False
        else:
            return True

    def _validate_commit_message_for_generic_type(self, match: str) -> bool:
        """Validates other commit types do not contain a scope"""
        type, scope, *_ = match.groups()
        if scope is None:
            return True
        else:
            self.error.generic_type_scope_error_message.append(
                f"Commits of type '{type}' must not specify a scope but simply use the form '{type}'"
            )
            return False
