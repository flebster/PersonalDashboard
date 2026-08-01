fetch("news.json")

.then(r => r.json())

.then(data => {

    const container =
        document.getElementById("articles");

    container.innerHTML = "";

    data.articles

        .sort((a,b)=>
            new Date(b.downloaded) -
            new Date(a.downloaded)
        )

        .forEach(article=>{

            const card =
                document.createElement("div");

            card.className="card";

            const date =
                new Date(article.downloaded);

            const formatted =
                date.toLocaleDateString(
                    undefined,
                    {
                        month:"short",
                        day:"numeric"
                    });

            card.innerHTML=`

<h2>${article.title}</h2>

<div class="meta">

${article.source}
 •
${formatted}

</div>

<div class="badge">

${article.category}

</div>

<div class="actions">

<button>

Read Article

</button>

</div>

`;

            container.appendChild(card);

        });

});
