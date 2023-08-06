'use strict'
const fs = require('fs');
const { default: Contato } = require('./contato.cjs');

module.exports = class Agenda {
	constructor(connection) {
		this.connection = connection
	}

	async listarContatos() {
		const sql = `
		SELECT
		nome,
		telefone,
		email,
		nascimento
		FROM agenda
		ORDER BY
		nome,
		nascimento DESC
		`
		const queryResult = await this.connection.query(sql)
		for (let i = 0; i < queryResult.rows.length; i++) {
			console.log(queryResult.rows[i].nome);
		}			
		this.connection.end()
	}

	async gravarContato(contato) {
		let sql = `
		SELECT nome, telefone, email
		FROM agenda
		WHERE telefone <> $1 AND email = $2
		`

		let values = [contato.telefone, contato.email]
		let queryResult = await this.connection.query(sql, values)
		let novo = !queryResult.rows.length > 0

        if (!novo) {
			const row = queryResult.rows[0]
            let mensagem = `Email ${row.email} já cadastrado para o Contato ${row.nome}, telefone ${row.telefone}`
            throw new Error(mensagem)
		}

        sql = "SELECT telefone FROM agenda WHERE telefone = $1"
		queryResult = await this.connection.query(sql, [contato.telefone])
		novo = !queryResult.rows.length > 0

        sql = "UPDATE agenda SET nome = $1, email = $2, nascimento = $3 WHERE telefone = $4"
        if (novo) sql = "INSERT INTO agenda (nome, email, nascimento, telefone) VALUES ($1, $2, $3, $4)"

        values = [contato.nome, contato.email, contato.nascimento, contato.telefone]
		queryResult = await this.connection.query(sql, values)

        return novo
	}

  	writeFile() {
		const jsonData = { "nome": "João", "idade": 30 };

		fs.writeFile('teste.json', JSON.stringify(jsonData), (err) => {
			if (err) {
			console.error(err);
			return;
			}
			console.log("Arquivo gravado com sucesso!");
		});
	}
}