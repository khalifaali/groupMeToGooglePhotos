# groupMeToGooglePhotos

Essentially the script will pull as many pictures as you want and save them in the current working directory in a folder named after the selected group chat.Then it will upload them to google photos.
<!DOCTYPE html>
<h1>Hey, I'm Khalif and welcome to groupMeToGooglePhotos</h1>

<p>For me the groupme gallery lacked the robustness of google photos and I found it quite hard to look for pictures because there was no way
to search for faces, places, etc. So I sat and decided that I will use the GroupMe API and Google Photos API to help me achieve this goal</p>

<p>The script is still a work in progress but as of right now you can load group messages, and save pictures in a directory named after
 the target groupchat. I have plans to add functionality to allow you to upload pictures to google photos within the next few days </p>


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

<br><em>Update</em> Added functionality so that when you download images it saves to them to a directory named after the groupchat.
I added an exception if the save folder exists in the current working directory it will just make that the save directory instead
of recreating the directory.

<h2> And thats all for now folks. Check back if you wanna see some more</h2>

<ul><em><b>Todo list</b></em>
 <li>V1.2 Enable an option that lets you select how many pictures are pulled back </li>
 <li>Write regex to remove invalid characters from groupme names</li>
 <li>Refactor https://github.com/khalifaali/groupMeToGooglePhotos/blob/dc10a7b91b88497871aea64167dab9583ee5624d/gm_parse.py#L111</li>
 <li>Figure out how to go back to first groupme message. Write method to return False if the method reaches the end. Perhaps if the
 before_id is the same after we flip the list then we know we are at the end...hmmmmm maybe pre-flip mess_id[0] == mess_id[-1] then return false..???</li>
  <li><strike>Figure out how to save photos on local storage</strike></li>
 <li>Successfully saved photos! I did have to save them to local storage so that I can upload using google photos API</li>
  <li>answer  ^^^ https://developers.google.com/photos/library/guides/upload-media </li>
  <li>Figure out how to add users in groupme to the shared album so that they can see photos</li>
  <li> <strike>Support to allow you to refresh messages in a more intuitive way.</strike></li>
   <li>I took out the test loops so you can write a loop around load_group_messages()</li>
 <li> <strike>Support to allow you to select how many messages you want to see per load</strike></li>
  <li>Support to allow script to connect to google photos API</li>
</ul>

<ul><em><b>Personal plans for script and other groupMe api projects</b></em>
<li>Move to this aws server to run script annually to collect new photos</li>
<li>Create functionality that when photos are selected to be copied the script knows to ignore photos that have already been uploaded. I will probably just have a csv that 
has a particular message id upload date that I use the signal to the script that everything before that date has been uploaded so abort operation.</li>
<li>Find nicer word for abort</li>
<li>Develop an @all mention feature via a bot</li>


