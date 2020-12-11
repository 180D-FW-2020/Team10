/*
Some things to note, 
  When creating the character you must give them a sprite that is not attached to the weapon
  then attatch a sprite weapon that rest in front of the character
  then you need to create an empty object that is attatched to the point (firepoint), just outside of the collider of the weapon
  For the character
    Attach a Rigidbody 2D
    Attach polygon collider 2d
    Attach Player (script)
    Attach character 2d controller (script)
    Attach Voice movement (script)
    Attach Speed (script)
  For the weapon  
    Attach Weapon_rotate (script)
    Attach M2MqttUnityClientRotate (script)
    Attaching a collider is optional here since the firepoint might hit the bow, only attach if you want object to collide with the weapon
  For the firepoint
    Attach Weapon (script)
    Attach M2MqttUnityClientFire (script)
    Attach M2MqttUnityClientReload (script)
    
For the Target board
  Create as many object connected to the original board
    Attach Box Colliders to the object
  there needs to be the same amount as there is areas to score on x2 since each color appears as an upper and lower. You can use 1 or two for the center
    Attach Points White to the object
    
For the title
  Make a TextMeshPro object
    optionally add a collider if you want to shoot it to get it destroyed or not, you would have to write this yourself
  Attach Dissapear_time_interval (Script) 
  
For Initial Scene you need to make a button
  here I made a text mesh bubble that states Start Game
    Attach To Next Scene (script) // This has it so that when something collides with you the game will move to the next scene which is the start time
    This script also has voice recognition in it so that you can start the game just by saying start
*/
