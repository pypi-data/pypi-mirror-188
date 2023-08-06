import librosa
from moviepy import editor
class AutoclipVolume:
    def __init__(self,path:str) -> None:
        self.clip = librosa.load(path)
        self.mps  = self.clip[1]
        self.alltime = len(self.clip[0])//self.mps
        self.maxvolume = max(self.clip[0])
        self.minvolume = min(self.clip[0])
        print(self.minvolume)
        print(self.maxvolume)
    def getmarklistbyvolume(self,volume:float,duration:int):
        avgvolume = []
        for idx in range(0,self.alltime//duration):
            segmentvolumegat = sum(self.clip[0][idx*duration*self.mps:(idx+1)*duration*self.mps])/(duration*self.mps)
            avgvolume.append(segmentvolumegat)
        minv = min(avgvolume)
        maxv = max(avgvolume)
        volumegate = (maxv-minv)*volume+minv
        
        volumecliplist =[]
        for idx in avgvolume:
            volumecliplist.append(idx>volumegate)
        return [duration,volumecliplist]
    def getmarklistbytime(self,finaltime:float,duration:int):
        returnlist = []
        for idx in range(0,10):
            returnlist = self.getmarklistbyvolume(1-idx/10.0,duration)
            if sum(returnlist[1])*returnlist[0]>finaltime*self.alltime:
                print(idx)
                return returnlist
class AutoclipVideo:
    def __init__(self,path:str) -> None:
        self.clip = editor.VideoFileClip(path)
    def clipandsave(self,savepath:str,cliplist:list):
        cliparr=[]
        for idx,keep in enumerate(cliplist[1]):
            if keep:
                segment = self.clip.subclip(idx*cliplist[0],(idx+1)*cliplist[0])
                # segment = self.clip.subclip(0,5)
                cliparr.append(segment)
        cp=editor.concatenate_videoclips(cliparr)
        cp.write_videofile(savepath)
def splitvolume(orginmp4:str,savemp3:str):
    v1 = editor.VideoFileClip(orginmp4)
    v1.audio.write_audiofile(savemp3)

if __name__=="__main__":
    import time
    splitvolume("233.mp4","233.mp3")
    time.sleep(3)
    xe = AutoclipVolume("233.mp3")
    # cc=xe.getmarklistbyvolume(0.5,5)
    # print(cc)
    cc=xe.getmarklistbytime(0.2,5)
    print(cc)
    time.sleep(3)
    xe = AutoclipVideo("233.mp4")
    xe.clipandsave("2333.mp4",cc)
