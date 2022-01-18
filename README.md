# SyntaxDB, a lightweight, easy-to-use, scalable serverless database.

I made SyntaxDB out of the frustration I have with modern server databases.

- They can be really resource intensive and expensive (MongoDB)
- They are obsolete, sluggish and don't work well with hosts now-a-days. (MySQL)
- They are server-less and decent, but can only process 1 query at a time. (SQLite)

My solution to all of that is: SyntaxDB!

Not only can you use this to store game settings and other things, but since it's serverless, it can EASILY run on any host that lets you make files and edit them without "security" reasons (sob sob, Replit)

# Features:
- It performs proper binary serialization and deserialization just like your average joe database.
- It can do "safe" conversion from old database files to another, for eg., maybe you try to convert a really old SDB database and something goes wrong, no worries! It makes a backup before starting conversion.
- It can load from JSON files, and dump data to JSON files, making it transport-able!
- It is fast and barely uses resources!
- It uses a parser for commands which even a child can learn! [function1 argument1(type) argument2(type)]
- If you make a mistake, no worries! SDB does not save your changes till you call [DUMP].

Future Features:
- It will be able to host a Flask/Werkzeug server which lets you transmit data from one server to another (password-encrypted, obviously!).
- Types, since it's typeless right now! I do fancy some types.

# Command Syntax:
Current:
function <args>
Future:
function <arg>(type) <arg2>(type)

# Commands:
DUMP: Save the file to your Python script's local directory as <dbname>.syntaxdb
JSONLOAD: Load data from a JSON file.
JSONDUMP: Dump data from a JSON file.
GET: Get data from a structure.

(Note: this is more of a hobby project and I'd rather quite fancy showing this to my teacher, to show that I'm not empty-headed!)
(Oh, also, I'll use this for my commercial projects, you can too!)
(This'll stay open-source forever too, btw, so it'll be getting updates frequently.)
(Please, if any of you security fellas are out there, please point out vulnerabilities.)
