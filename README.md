# groupMeToGooglePhotos
This script allows you to connect to groupme and pull all associated images and push them to google photos...Atleast I hope so lol. Gotta look at Google Photos API and see if I can get download the image from groupme cdn.
<!DOCTYPE html>
<h1>Hey, I'm Khalif and welcome to groupMeToGooglePhotos</h1>

<p>For me the groupme gallery lacked the robustness of google photos and I found it quite hard to look for pictures because there was no way
to search for faces, places, etc. So I sat and decided that I will use the GroupMe API and Google Photos API to help me achieve this goal</p>

<p>The script is still a work in progress but as of right now you can load group messages, and find pictures. I have plans to add upload
 pictures to google photos within the next few days </p>


<h2>Here is an example of how to use the code that I have written</h2>

<pre>

from gm_parse import Gm_Parser as g_parser

gp = g_parser('insert access token')
gp.get_groups()

gp.select_group_messages()
gp.load_group_messages()

</pre>


<h3> import Gm_Parser </h3>
You will need to import the Gm_Parser class from the gm_parse file
I chose to do the following
<br><code>from gm_parse import Gm_Parser as g_parser</code>

<h3> Set access token and application name </h3>
Here you will need to pass your access token given to you by the GroupMe API services
<br><code>gp = g_parser('insert access token')</code>

<h3>Retrieve groupchats</h3>
To get some of your available groupchats call the get_groups which will return an array of dictionaries that will have your groupchat name and groupchat ids'
<br><code>gp.get_groups()</code>

<h3>Select a groupchat</h3>
You will need to call get_groups() before you call this method. Once you do this, a prompt will present itself telling you to select a groupchat
to display its respective messages
<br><code>gp.select_group_messages()</code>

<h3>Display groupchat messages</h3>
You will need to call select_group_messages() before you call this method. once you do this, some of the messages will display( ~600 ) will display.
I will allow you to set limits when I have some more time, this is what I used for testing.
<br><code>gp.load_group_messages()</code>

<h2> And thats all for now folks. Check back if you wanna see some more</h2>

<ul><em><b>Future Updates</b></em>
  <li>Figure out how to save photos. Will I have to save them to local storage then upload?</li>
  <li>answer  ^^^ https://developers.google.com/photos/library/guides/upload-media </li>
  <li>Figure out how to add users in groupme to the shared album so that they can see photos</li>
  <strike><li>Support to allow you to refresh messages in a more intuitive way.</li>
   <li>I took out the test loops so you can write a loop around load_group_messages()</li>
  <strike><li>Support to allow you to select how many messages you want to see per load</li>
  <li>Support to allow script to connect to google photos API</li>
</ul>

<ul><em><b>Personal plans for script and other groupMe api projects</b></em>
<li>Move to this aws server to run script annually to collect new photos</li>
<li>Create functionality that when photos are selected to be copied the script knows to ignore photos that have already been uploaded. I will probably just have a csv that 
has a particular message id upload date that I use the signal to the script that everything before that date has been uploaded so abort operation.</li>
<li>Find nicer word for abort</li>
<li>Develop an @all mention feature via a bot</li>


