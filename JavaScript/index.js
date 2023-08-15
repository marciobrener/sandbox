// const { Agenda } = require("./agenda.cjs")
// import Agenda from '/.agenda.cjs';
const Agenda = require("./agenda.cjs")
const { Client } = require("pg")

const dotenv = require("dotenv")
// import * as dotenv from 'node:dotenv';
dotenv.config()
 
class Runner {
    constructor(config) {
        this.connection = new Client({
            user: process.env.PGUSER,
            host: process.env.PGHOST,
            database: process.env.PGDATABASE,
            password: process.env.PGPASSWORD,
            port: process.env.PGPORT
        })

        const f = async () => await this.connection.connect()
        f()
    }

    async run() {
        const agenda = new Agenda(this.connection)
        // agenda.cadastrarContato(contato)
        await agenda.listarContatos()
    }
}

const f = async() => {
    try {
        const runner = new Runner()
        await runner.run()
        console.log("Fim")
    } catch (exception) {
        console.log(exception)
    } finally {
        console.log("finally")
    }    
}

f()