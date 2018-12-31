# groupMeToGooglePhotos

Essentially the script will pull as many pictures and videos you want and save them in the current working directory in a folder named after the selected group chat. All media saved will be named after its message ID given by groupme. Then it will upload that saved media to google photos. Written using Python 3.7.0
<!DOCTYPE html>
<h1>Hey, I'm Khalif and welcome to groupMeToGooglePhotos</h1>

<p>For me the groupme gallery lacked the robustness of google photos and I found it quite hard to look for pictures because there was no way
to search for faces, places, etc. So I sat and decided that I will use the GroupMe API and Google Photos API to help me achieve this goal</p>

<p>The script is still a work in progress but as of right now you can load group messages, and save pictures in a directory named after
 the target groupchat. I have plans to add functionality to allow you to upload pictures to google photos within the next few days </p>


<h2>Here is an example of how to use the code that I have written</h2>

<pre>

from gm_parse import Gm_Parser as g_parser

gp = g_parser('set access token')
gp.get_groups()
gp.select_group_messages()
while gp.load_group_messages(): 
    continue
print('Done')


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

<h3>Save media</h3>
You will need to call select_group_messages() before you call this method. <code>load_group_messages()</code> pulls back group messages, and calls the <code> save_media()</code> function to download media from the groupMe gallery. The function will return True if there are more messages that can be loaded.
I will allow you to set limits when I have some more time, this is what I used for testing.
<br><code>gp.load_group_messages()</code>

<br><em>Update</em> Added functionality so that when you download images it saves to them to a directory named after the groupchat.
I added an exception if the save folder exists in the current working directory it will just make that the save directory instead
of recreating the directory.

<h2>Optional Functions/Arguments for functions</h2>
+Set amount of pictures and videos you want to save by providing a number to the amount argument. If no limit is present will save all images in group message gallery. Currently I haven't developed a solution to pull back just pictures or just videos. Suggested update could be to pass an optional flag into load messages that lets you specify what media you want back

<code>set_media_limit(amount)</code><br>
  --This must be called before load_group_messages() to take effect.

+Set amount of messages displayed by assigning a number to txts_per_page keyword argument
<code>load_group_messages(txts_per_page=None)</code>

+Set amount of group chats displayed by providing a number for the amount argument. Default is 10, no max was given in GroupMe API documentation<br>
<code>set_groups_per_page(amount):</code><br>
 --This must be called before get_groups() to take effect.




<h2> And thats all for now folks. Check back if you wanna see some more</h2>


<ul><em><b>Todo list</b></em>
 <li><strike>Add logic so that if an album exists it doesnt create it again</strike></li>
 <li>Add option to add allow user to post shareable link to their groupchat. (However,will always display on console regardless)</li>
 <li>Need to make method to pull back filenames of media items in Target upload directory</li>
 <li>Refactor gp_upload code into a class</li>
 <li>Allow for access token to be given via command line argument</li>
 <li>Make sure dependancies can be easily installed</li>
 <li>v1.3 Add support to allow you to control what type of media you want pulled back whether it be pictures or videos</strike></li> 
 <li><strike>Rename anything that has pix in its name to media o that is agnostic to the user and more fluid</strike></li>
 <li>After photos have been uploaded to Google Photos get shareable link</li>
 <li><strike>V1.2 Enable an option that lets you select how many pictures are pulled back</strike> </li>
 <li><strike>v1.2Enable option to allow you to select how many groups are shown</strike></li>
 <li><strike>Write regex to remove invalid characters from groupme names</strike></li>
 <li><strike>Refactor https://github.com/khalifaali/groupMeToGooglePhotos/blob/dc10a7b91b88497871aea64167dab9583ee5624d/gm_parse.py#L111</strike></li>
 <li><strike>Figure out how to go back to first groupme message. Write method to return False if the method reaches the end. Perhaps if the
 before_id is the same after we flip the list then we know we are at the end...hmmmmm maybe pre-flip mess_id[0] == mess_id[-1] then return false..???</strike></li>
  <li><strike>Figure out how to save photos on local storage</strike></li>
  <li>Review https://developers.google.com/photos/library/guides/upload-media to connect Google Photos API</li>
  <li> <strike>Support to allow you to refresh messages in a more intuitive way.</strike></li>
 <li><strike>Support to allow you to select how many messages you want to see per load</strike></li>
</ul>

<ul><em><b>Personal plans for script and other groupMe api projects</b></em>
<li>Move to this aws server to run script annually to collect new photos</li>
<li>Create functionality that when photos are selected to be copied the script knows to ignore photos that have already been uploaded. I will probably just have a csv that 
has a particular message id upload date that I use the signal to the script that everything before that date has been uploaded so abort operation.</li>
<li>Find nicer word for abort</li>
<li>Develop an @all mention feature via a bot</li>


