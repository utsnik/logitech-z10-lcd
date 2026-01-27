# Powershell script to get Windows Media Info
# Returns "Artist | Title | Album | PositionSeconds | DurationSeconds"
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]

function Await($WinRtTask, $ResultType) {
    $asTaskGeneric = $asTask.MakeGenericMethod($ResultType)
    $netTask = $asTaskGeneric.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}

[Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager, Windows.Media.Control, ContentType = WindowsRuntime] | Out-Null
$manager = Await ([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager]::RequestAsync()) ([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionManager])

$session = $manager.GetCurrentSession()
if ($session) {
    # Get Metadata
    $info = Await ($session.TryGetMediaPropertiesAsync()) ([Windows.Media.Control.GlobalSystemMediaTransportControlsSessionMediaProperties])
    
    # Get Timeline
    $timeline = $session.GetTimelineProperties()
    $pos = $timeline.Position.TotalSeconds
    $dur = $timeline.EndTime.TotalSeconds
    
    # Format: Artist | Title | Album | Pos | Dur
    Write-Output "$($info.Artist)|$($info.Title)|$($info.AlbumTitle)|$([math]::Round($pos))|$([math]::Round($dur))"
}
else {
    Write-Output "Stopped|No Media||0|1"
}
