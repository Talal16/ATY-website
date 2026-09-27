import os
from moviepy import ColorClip, TextClip, CompositeVideoClip, vfx
import arabic_reshaper
from bidi.algorithm import get_display

def get_arabic_text(text):
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

scenes = [
    {
        "start": 0, "end": 6,
        "title": "SCENE 01 — THE STRUGGLE",
        "description": "Black screen. Keyboard typing sound.\nSHOT 1: Extreme Close-Up of student's eye. Tablet reflects.\nSHOT 2: Over-The-Shoulder. Trying to code on a tablet.\nSHOT 3: Top Shot. Cluttered small desk.",
        "vo": "بتتعلم برمجة... وكل حاجة قدامك على شاشة واحدة؟"
    },
    {
        "start": 6, "end": 9,
        "title": "SCENE 02 — THE QUESTION",
        "description": "Student stops. Looks up.\nSHOT 4: Slow push-in to face, cut to black.",
        "vo": "طب... ليه تغيّر جهازك؟"
    },
    {
        "start": 9, "end": 16,
        "title": "SCENE 03 — THE TRANSFORMATION",
        "description": "Electronic music drops.\nSHOT 5: Macro of Galaxy Tab A9+ on stand.\nSHOT 6: Orbit shot around tablet/stand/keyboard/mouse.\nSHOT 7: Whip Pan to monitor. Screen reveals.",
        "vo": "غيّر الـ Setup.\n\nYOUR TABLET.\nA BETTER WORKSPACE."
    },
    {
        "start": 16, "end": 23,
        "title": "SCENE 04 — THE SETUP",
        "description": "Fast Montage.\nSHOT 8: Keyboard click.\nSHOT 9: Mouse moves.\nSHOT 10: Samsung DeX opens.\nSHOT 11: Slider shot of full setup.\nSHOT 12: Hero reveal of student + full setup.",
        "vo": "Stand... Keyboard... Mouse... وشاشة أكبر.\n\nكل حاجة في مكانها."
    },
    {
        "start": 23, "end": 32,
        "title": "SCENE 05 — THE REAL EXPERIENCE",
        "description": "Music builds.\nSHOT 13: Overhead of full setup.\nSHOT 14: Tracking behind shoulder. Monitor shows IDE.\nSHOT 15: Extreme macro of rapid typing.\nSHOT 16: Rack focus from fingers to screen.\nSHOT 17: Side track, student coding.",
        "vo": "تابع الشرح على مساحة أكبر...\n\nوطبّق بإيدك."
    },
    {
        "start": 32, "end": 37,
        "title": "SCENE 06 — THE TRANSFORMATION PAYOFF",
        "description": "SHOT 18: 360° Orbit around student and setup.\nLighting changes dynamically.\nTablet, Monitor, Keyboard, Mouse, Student all in frame.",
        "vo": "نفس التابلت اللي معاك...\n\nلكن تجربة مختلفة تمامًا."
    },
    {
        "start": 37, "end": 42,
        "title": "SCENE 07 — PRODUCT HERO",
        "description": "Music softens.\nSHOT 19: Hero Shot. Slow cinematic push-in.\nForeground: Tablet + Stand + KB + Mouse.\nBackground: Monitor (Shallow DoF).\n\nSTARTER vs FULL SETUP displayed.",
        "vo": "اختار الـ Setup المناسب ليك."
    },
    {
        "start": 42, "end": 45,
        "title": "SCENE 08 — FINAL CTA",
        "description": "SHOT 20: Final push-in to Tablet.\nScreen: READY TO BUILD?\nLogo, WhatsApp, QR Code.",
        "vo": "ابعتلنا موديل التابلت... ونجهزلك الـ Setup المناسب.\n\nYOUR TABLET.\nYOUR WORKSPACE.\nYOUR NEXT STEP."
    }
]

font_path = "fonts/Amiri-1.000/Amiri-Bold.ttf"
w, h = 1920, 1080

clips = []

for i, scene in enumerate(scenes):
    duration = scene["end"] - scene["start"]

    # Background
    bg = ColorClip(size=(w, h), color=(15, 15, 20), duration=duration)

    # Scene Title
    title_text = scene["title"]
    title_clip = TextClip(
        font=font_path,
        text=get_arabic_text(title_text),
        font_size=60,
        color='white',
        size=(w, 100),
        method='label'
    ).with_position(('center', 100)).with_duration(duration)

    # Timestamp
    time_text = f"T: {scene['start']}s - {scene['end']}s"
    time_clip = TextClip(
        font=font_path,
        text=time_text,
        font_size=40,
        color='#ff5555',
        size=(w, 80),
        method='label'
    ).with_position(('center', 50)).with_duration(duration)

    # Description (Action)
    desc_text = scene["description"]
    desc_clip = TextClip(
        font=font_path,
        text=get_arabic_text(desc_text),
        font_size=40,
        color='#aaaaaa',
        size=(int(w*0.8), 400),
        method='caption',
        text_align='center'
    ).with_position(('center', 250)).with_duration(duration)

    # Voice Over
    vo_text = scene["vo"]
    if vo_text:
        vo_clip = TextClip(
            font=font_path,
            text=get_arabic_text(vo_text),
            font_size=50,
            color='#55ff55',
            size=(int(w*0.8), 300),
            method='caption',
            text_align='center'
        ).with_position(('center', 700)).with_duration(duration)

        comp = CompositeVideoClip([bg, title_clip, time_clip, desc_clip, vo_clip], size=(w, h)).with_duration(duration)
    else:
        comp = CompositeVideoClip([bg, title_clip, time_clip, desc_clip], size=(w, h)).with_duration(duration)

    # Optional fade transition between scenes (except for the first)
    if i > 0:
        comp = comp.with_effects([vfx.CrossFadeIn(0.5)])
        # we need to adjust start time for crossfade if we were merging them, but simple concatenation is fine for now

    clips.append(comp)

from moviepy import concatenate_videoclips

final_video = concatenate_videoclips(clips, method="compose")
final_video.write_videofile("student_coding_station_animatic.mp4", fps=24, codec="libx264")
