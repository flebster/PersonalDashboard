/*
Personal Dashboard
Version 7.0
Main dashboard application
*/


let articles = [];


/*
Load the article database
*/

async function loadArticles() {

    try {

        const response = await fetch("news.json");


        if (!response.ok) {

            throw new Error(
                "Could not load news.json"
            );

        }


        const data = await response.json();


        articles = data.articles || [];


        updateStatus();


        renderArticles(articles);


    } catch (error) {


        console.error(
            error
        );


        document.getElementById(
            "status"
        ).textContent =
            "Unable to load articles";

    }

}



/*
Update dashboard status
*/

function updateStatus() {


    const unread = articles.filter(
        article =>
            !article.read
    ).length;


    document.getElementById(
        "status"
    ).textContent =

        `${articles.length} articles • ${unread} unread`;

}



/*
Create article cards
*/

function renderArticles(articleList) {


    const container =
        document.getElementById(
            "articles"
        );


    container.innerHTML = "";


    if (articleList.length === 0) {


        container.innerHTML = `

            <div class="card">

                <h2>
                    No articles found
                </h2>

                <p>
                    Try another search.
                </p>

            </div>

        `;


        return;

    }



    articleList.forEach(
        article => {


        const card =
            document.createElement(
                "article"
            );


        card.className =
            "card";



        const title =
            escapeHTML(
                article.title || 
                "Untitled article"
            );


        const source =
            escapeHTML(
                article.source || 
                "Unknown source"
            );


        const category =
            escapeHTML(
                article.category || 
                "General"
            );



        /*
        The article file is stored as:
        articles/year/month/source/file.html

        The web folder is one level above it.
        */

        const articleLink =
    article.file;


        card.innerHTML = `

            <h2>
                ${title}
            </h2>


            <div class="source">

                ${source}

            </div>


            <div class="category">

                ${category}

            </div>


            <br>


            <a href="${articleLink}">

                Read Article →

            </a>

        `;



        container.appendChild(
            card
        );


    });

}



/*
Search function
*/

document
    .getElementById("search")
    .addEventListener(
        "input",
        function(event) {


        const term =
            event.target.value
            .toLowerCase();



        const filtered =
            articles.filter(
                article => {


                const title =
                    (
                    article.title || ""
                    )
                    .toLowerCase();


                const source =
                    (
                    article.source || ""
                    )
                    .toLowerCase();


                const category =
                    (
                    article.category || ""
                    )
                    .toLowerCase();



                return (

                    title.includes(term) ||

                    source.includes(term) ||

                    category.includes(term)

                );


            });



        renderArticles(
            filtered
        );


    });



/*
Basic HTML safety
*/

function escapeHTML(text) {


    return text
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

}



/*
Start dashboard
*/

loadArticles();
