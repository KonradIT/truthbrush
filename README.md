# truthbrush
API client for Truth Social

**NOTE: My `main` branch is meant for running an archiver of truths, and the other branches will be for fixes/new features etc...**

## CLI:

```text
Commands:
  followers    Pull a user's followers.
  following    Pull users a given user follows.
  search       Search for users, statuses or hashtags.
  statuses     Pull a user's statuses
  suggestions  Pull the list of suggested users.
  tags         Pull trendy tags.
  trends       Pull trendy Truths.
  user         Pull a user's metadata.
```

## Scripts:

- `archive-truths.py`: Script to archive Truth Social posts from several key profiles. Runs every day at 00:00 (GitHub Machine Time). See `output` for archived truths.