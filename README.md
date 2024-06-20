<h1> RECIPE SHARING WEBSITE</h1>
<h4>It is a project about a recipe sharing website using the framework django.</h4>
<h4>It is very simple because it is focused on backend using the framework django</h4>
<h3>Implements:</h3>
  <ul>
    <li>
      user register/login/logout logic and templates
    </li>
    <li>
      add recipe logic/template mixed with add ingredients logic/template so it is more realistic
    </li>
    <li>
      possibility to save recipes and a logic to count how much ppeople save it and displa this number
    </li>
    <li>
      a function to manage the images (resize and default image)
    </li>
    <li>
      search recipes by title
    </li>
</ul>
<p>
  User can search and see the details about recipes without do the login, but if you register/login User can write recipes, save it on his favourites and take a look on them
  When an user create a recipe have to choose an image (if not there is a default image), a title, description, the istructions, the category (is a manytomany relationship so he can choose more than one and there   are already in the website added by the admins) and other feature. User can add/remove like and save/remove it on his profile thanks to a button. Admin and staff can delete any recipes whitout being the author.
  We can see all the categories and from them we can see all the recipes associated with the category.
  For interface it is used bootstrap.
</p>
<div>
<i> Riscontrato alcuni problemi dopo il deployment nella visualizzazione delle immagini e certe funzioni di bootstrap estetiche. Vengono salvate nel database, ma il sito non riesce a mostrarle (cosa che non accadeva prima del deployment)</i>
</div>

  
  
