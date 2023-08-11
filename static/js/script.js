$(document).ready(function () {
    listing();
});

function listing() {
    fetch('/game_ranking').then((res) => res.json()).then((data) => {
        let rows = data['result']
        $('#game-rank').empty()
        rows.forEach(a => {
            let rank = a['rank']
            let icon_url = a['icon_url']
            let name = a['name']
            let company = a['company']
            let genre = a['genre']
            let pay = a['pay']
            
            let temp_html = `<tr class="ranking-table-rows">
                                <td>
                                    <id="game_rank"> <span class="rank red">${rank}</span>
                                </td>
                                <td>
                                    <img id="game_icon" class="game-icon" src="${icon_url}">
                                </td>
                                <td>
                                    <div id="game_name" class="game-name">${name}</a></div>
                                </td>
                                <td>
                                    <div class="game-info">
                                        <p id="game_company" class="company">${company}</a></p>
                                        <span id="game_genre">${genre}</span> |
                                        <span id="game_pay">${pay}</span>
                                    </div>
                                </td>
                            </tr>`
            $('#game-rank').append(temp_html)
        })
    })
}