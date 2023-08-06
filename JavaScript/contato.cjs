module.exports = class Contato {
    static getIntance(contato) {
        return new Contato(contato[0], contato[1], contato[2], contato[3])
    }

    constructor (nome, telefone, email, nascimento) {
        this.nome = nome
        this.telefone = telefone
        this.email = email
        this.nascimento = nascimento
    }
}