
https://askubuntu.com/questions/28496/how-do-i-setup-an-icecast-server-for-broadcasting-audio-in-my-network

here is an example howto stream using ffmpeg to icecast
https://www.streamingmediaglobal.com/Articles/Editorial/Featured-Articles/DIY-Live-Audio-Streaming-Using-Icecast-with-FFmpeg-125665.aspx?utm_source=related_articles&utm_medium=gutenberg&utm_campaign=editors_selection
http://linux-audio.4202.n7.nabble.com/stream-from-jack-to-icecast-2-td109362.html#a109380


ffmpeg -f jack -ac 2 -i ffmpeg -acodec libmp3lame -ab 128k -f mp3 icecast://source:<password>@localhost:8000/stream