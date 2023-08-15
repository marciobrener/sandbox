const { Client } = require("pg")
const Agenda = require("./agenda.cjs")
const Contato = require("./contato.cjs")

var connection = null

async function test_conectar_banco() {
    if (!connection) {
        connection = new Client({
            user: process.env.PGUSER,
            host: process.env.PGHOST,
            database: process.env.PGDATABASE,
            password: process.env.PGPASSWORD,
            port: process.env.PGPORT
        })
    
        await connection.connect()
    }

    return connection
}

async function test_gravar_contato() {
    const connection = await test_conectar_banco()

    let values = ['Jose', '5853896', 'jose@xpto.com', '1978-12-31']
    values = ['Mario', '35246', 'jose@xpto.com', '1978-12-31']
    let contato = Contato.getIntance(values)

    const agenda = await new Agenda(connection)
    await agenda.gravarContato(contato)
    .then(value => {
        return value
    })
    .catch(err => {
        return err
    })
}

async function test_desconectar_banco() {
    if (connection) await connection.end()
}

//jest --detectOpenHandles
//npm t

// module.exports = { test_intanciar_agenda }
test_gravar_contato()
it ('Conectar banco', async () => await test_conectar_banco)
it ('Gravar contato', async () => 
    await expect(test_gravar_contato(),).resolves.not.toThrowError()
)

it ('Desconectar banco', async () => 
    await expect(test_desconectar_banco(),).resolves.not.toThrowError()
)