from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parent
entries=[]
for phase,start,end in [(5,38.45,39.98),(13,46.10,47.61)]:
 for speed,mult in [('normal',1),('quarter',4)]:
  dest=R/f'native-phase-{phase:02d}-{speed}.mp4'
  vf=f'trim=start={start}:end={end},setpts={mult}*(PTS-STARTPTS),transpose=2,crop=2112:978:0:0'
  subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-v','error','-i',str(R/'settle-native.mov'),'-vf',vf,'-an','-fps_mode','passthrough','-enc_time_base','1:60000','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(dest)],check=True)
  data=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','stream=nb_frames,duration','-of','json',str(dest)]))['streams'][0]
  entries.append({'file':dest.name,'start':start,'end':end,'timeScale':mult,**data})
(R/'native-export.json').write_text(json.dumps(entries,indent=2)+'\n')
print(entries)
