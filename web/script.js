fetch("../news.json")

.then(response => response.json())

.then(data => {


    let container =
        document.getElementById("articles");


    container.innerHTML="";


    data.articles.forEach(article => {


        let card =
        document.createElement("div");


        card.className="card";


        card.innerHTML = `

        <h2>
        ${article.title}
        </h2>


        <p class="source">

        ${article.source || ""}

        </p>


        <button>

        Read Article

        </button>

        `;


        container.appendChild(card);


    });


});
