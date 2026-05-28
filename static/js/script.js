// FIFA 2026 AI Predictor - Main JavaScript

// Fetch teams and populate selects
async function loadTeams() {
    try {
        const response = await fetch('/api/teams');
        const teams = await response.json();
        const teamList = Object.keys(teams).sort();
        populateSelects(teamList);
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

function populateSelects(teams) {
    const team1Select = document.getElementById('team1');
    const team2Select = document.getElementById('team2');
    
    if (team1Select) {
        teams.forEach(team => {
            const option = document.createElement('option');
            option.value = team;
            option.textContent = team;
            team1Select.appendChild(option);
        });
    }
    
    if (team2Select) {
        teams.forEach(team => {
            const option = document.createElement('option');
            option.value = team;
            option.textContent = team;
            team2Select.appendChild(option);
        });
    }
}

// Predict match
async function predictMatch() {
    const team1 = document.getElementById('team1')?.value;
    const team2 = document.getElementById('team2')?.value;
    
    if (!team1 || !team2) {
        alert('Please select both teams');
        return;
    }
    
    if (team1 === team2) {
        alert('Please select different teams');
        return;
    }
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ team1, team2 })
        });
        
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Prediction failed');
        }
        displayPredictionResult(result);
    } catch (error) {
        console.error('Error predicting match:', error);
        alert(error.message || 'Error predicting match');
    }
}

function displayPredictionResult(result) {
    let html = `
        <div class="result-container">
            <div class="result-box">
                <div class="team-name">${result.team1}</div>
                <div class="probability">${result.team1_win_prob.toFixed(1)}%</div>
                <div class="prob-label">Win Probability</div>
            </div>
            <div class="result-box">
                <div class="team-name">${result.team2}</div>
                <div class="probability">${result.team2_win_prob.toFixed(1)}%</div>
                <div class="prob-label">Win Probability</div>
            </div>
        </div>
        <div class="card">
            <div class="kicker">Prediction Output</div>
            <h3>Prediction Details</h3>
            <div class="grid-2">
                <div class="stat-box">
                    <div class="stat-label">Predicted Winner</div>
                    <div class="stat-value">${result.predicted_winner}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Predicted Score</div>
                    <div class="stat-value">${result.predicted_score}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Draw Probability</div>
                    <div class="stat-value">${result.draw_prob.toFixed(1)}%</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Confidence</div>
                    <div class="stat-value">${Math.max(result.team1_win_prob, result.team2_win_prob, result.draw_prob).toFixed(1)}%</div>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('predictionResult').innerHTML = html;
}

// Simulate Tournament
async function simulateTournament() {
    try {
        const response = await fetch('/api/tournament-simulate', {
            method: 'POST'
        });
        
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Simulation failed');
        }
        displayTournamentResult(result);
    } catch (error) {
        console.error('Error simulating tournament:', error);
        alert(error.message || 'Error simulating tournament');
    }
}

function displayTournamentResult(result) {
    let html = `
        <div class="card">
            <div class="kicker">Simulation Output</div>
            <h2>🏆 Tournament Simulation Results</h2>
            
            <h3 style="margin-top: 1rem;">Semi-Finals</h3>
            <table>
                <tr>
                    <th>Match</th>
                    <th>Winner</th>
                    <th>Confidence</th>
                </tr>
    `;
    
    result.matches.forEach((match, idx) => {
        html += `
            <tr>
                <td>${match.team1} vs ${match.team2}</td>
                <td style="font-weight: 700; color: #7dff9b;">${match.winner}</td>
                <td>${match.prob}%</td>
            </tr>
        `;
    });
    
    html += `
            </table>
            
            <div class="card" style="margin-top: 1rem;">
                <div class="kicker">Final</div>
                <h3>🥇 Final Prediction</h3>
                <div class="grid-2">
                    <div class="stat-box">
                        <div class="stat-label">Team 1</div>
                        <div class="stat-value">${result.final.team1}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Team 2</div>
                        <div class="stat-value">${result.final.team2}</div>
                    </div>
                </div>
                <div class="center" style="margin-top: 1rem;">
                    <div style="font-size: 2rem; color: #7dff9b; font-weight: 700;">
                        🏆 ${result.final.predicted_winner}
                    </div>
                    <div class="subtle" style="font-size: 1.05rem; margin-top: 0.65rem;">
                        Champion Confidence: <span style="color: #7dff9b; font-weight: 700;">${result.final.confidence}%</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('tournamentResult').innerHTML = html;
}

// Load teams on page load
document.addEventListener('DOMContentLoaded', loadTeams);
