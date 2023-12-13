// json-server --watch _db/index.js --port 3000

const betting_odds = require('./betting-odds.json');
const box_score = require('./box-score.json')
const full_schedule = require('./full-schedule.json')
const sleeper_players = require('./sleeper-player-list.json')
const tank_players = require('./tank01-player-list.json')

module.exports = () => ({
    getNFLBettingOdds: betting_odds,
    getNFLBoxScore: box_score,
    getNFLGamesForWeek: full_schedule,
    getNFLPlayerList: tank_players,
    sleeper_players: sleeper_players,
});

