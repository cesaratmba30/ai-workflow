<#
.SYNOPSIS
  Install ai-workflow skills into an agent's skills directory (Windows/PowerShell).
  Non-destructive: an existing destination is backed up (never deleted) before
  being replaced, and you're asked to confirm unless -Yes is passed.

.PARAMETER Targets
  claude | codex | both (default: both)

.PARAMETER Project
  Install into the current project (.claude/skills, .codex/skills) instead of
  the user's home directory.

.PARAMETER Copy
  Copy instead of symlink (default: symlink -- creating a symlink on Windows
  may require Developer Mode or an elevated shell; use -Copy to avoid that).

.PARAMETER Yes
  Don't prompt before replacing an existing skill.

.PARAMETER DryRun
  Print what would happen, change nothing.

.PARAMETER BackupDir
  Put backups under this directory (default: <repo>\.install-backups\<timestamp>).

.EXAMPLE
  scripts/install.ps1 claude -Project -Copy -Yes
#>
param(
    [Parameter(Position = 0)]
    [ValidateSet("claude", "codex", "both")]
    [string]$Targets = "both",
    [switch]$Project,
    [switch]$Copy,
    [switch]$Yes,
    [switch]$DryRun,
    [string]$BackupDir
)

$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $PSScriptRoot
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
if (-not $BackupDir) {
    $BackupDir = Join-Path $RepoDir ".install-backups\$Timestamp"
}

function Confirm-Replace {
    param([string]$Message)
    if ($Yes) { return $true }
    if (-not [Environment]::UserInteractive) {
        Write-Warning "  SKIP: $Message (non-interactive; re-run with -Yes to replace)"
        return $false
    }
    $reply = Read-Host "  $Message [y/N]"
    return ($reply -match '^(y|yes)$')
}

function Test-AlreadyCorrect {
    param([string]$Dest, [string]$Src)
    if (-not (Test-Path -LiteralPath $Dest)) { return $false }
    $item = Get-Item -LiteralPath $Dest -Force
    if ($item.LinkType -eq "SymbolicLink") {
        $linkTarget = (Get-Item -LiteralPath $Dest).Target
        return ($linkTarget -eq $Src)
    }
    if ($Copy) {
        $diff = Compare-Object -ReferenceObject (Get-ChildItem -Recurse -File -LiteralPath $Src) `
                                -DifferenceObject (Get-ChildItem -Recurse -File -LiteralPath $Dest) `
                                -Property Name -ErrorAction SilentlyContinue
        return (-not $diff)
    }
    return $false
}

function Install-Into {
    param([string]$Dest)
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    $installed = 0; $skipped = 0; $backedUp = 0
    Get-ChildItem -Directory (Join-Path $RepoDir "skills") | ForEach-Object {
        $name = $_.Name
        $src = $_.FullName
        $target = Join-Path $Dest $name

        if (Test-Path -LiteralPath $target) {
            if (Test-AlreadyCorrect -Dest $target -Src $src) {
                return
            }
            if (-not (Confirm-Replace "$name already exists at $target -- back it up and replace it?")) {
                $skipped++
                return
            }
            if ($DryRun) {
                Write-Host "  [dry-run] would back up $target -> $BackupDir\$name"
            }
            else {
                New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
                Move-Item -LiteralPath $target -Destination (Join-Path $BackupDir $name)
                $backedUp++
            }
        }

        if ($DryRun) {
            $mode = if ($Copy) { "copy" } else { "link" }
            Write-Host "  [dry-run] would $mode $src -> $target"
        }
        else {
            if ($Copy) {
                Copy-Item -Recurse -LiteralPath $src -Destination $target
            }
            else {
                New-Item -ItemType SymbolicLink -Path $target -Target $src | Out-Null
            }
        }
        $installed++
    }
    $modeLabel = if ($Copy) { "copy" } else { "link" }
    Write-Host "Installed $installed skill(s) -> $Dest ($modeLabel)"
    if ($skipped -gt 0) {
        Write-Host "  Skipped $skipped existing skill(s) (declined or non-interactive)."
    }
    if ($backedUp -gt 0) {
        Write-Host "  Backed up $backedUp replaced skill(s) -> $BackupDir"
    }
}

$baseClaude = if ($Project) { ".claude\skills" } else { Join-Path $HOME ".claude\skills" }
$baseCodex  = if ($Project) { ".codex\skills" }  else { Join-Path $HOME ".codex\skills" }

switch ($Targets) {
    "claude" { Install-Into $baseClaude }
    "codex"  { Install-Into $baseCodex }
    "both"   { Install-Into $baseClaude; Install-Into $baseCodex }
}
