package sandbox;

import java.io.*;
import java.sql.*;

public class App implements Agenda {
    private static Connection connection;

    public App() throws SQLException {
        conectarBanco(true);
        criarAgenda();
    }

    private void conectarBanco(boolean postgres) throws SQLException {
        File file = new File("C:/Backup/MEUSDO~1/GitHub/sandbox/Sandbox/agenda.db");
        String url = String.format("jdbc:sqlite:%s", file);

        String user = null;
        String password = null;

        if (postgres) {
            user = "postgres";
            password = "postgres";
            url = "jdbc:postgresql://localhost:5432/";
        }

        connection = DriverManager.getConnection(url, user, password);
    }


    @Override
    public Contato entrarContato() throws IOException {
        Contato contato = new Contato();

        System.out.print("Nome: ");
        contato.nome = System.console().readLine();
        if (contato.nome.length() == 0) return contato;

        System.out.print("Telefone: ");
        contato.telefone = System.console().readLine();

        System.out.print("Email: ");
        contato.email = System.console().readLine();

        return contato;
    }

    public void apagarAgenda() throws SQLException {
        var sql = "DROP TABLE Agenda;";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        preparedStatement.execute();
        preparedStatement.close();
    }

    public void criarAgenda() throws SQLException {
        DatabaseMetaData databaseMetaData = connection.getMetaData();

        var sql = """
        CREATE TABLE Agenda (
            Telefone VARCHAR(15) PRIMARY KEY,
            Nome VARCHAR(100) NOT NULL,
            Email VARCHAR(256) NULL UNIQUE
        );

        CREATE INDEX Nome ON Agenda (Nome);
        """;

        ResultSet resultSet = databaseMetaData.getTables(null, null, "%Agenda", null);
        if (!resultSet.next()) connection.createStatement().execute(sql);
    }

    public void carregarContatos(String file) throws Exception {
        carregarContatos(new File(file));
    }

    @Override
    public void carregarContatos(File file) throws Exception {
        var reader = new BufferedReader(new FileReader(file));
        String texts[] = null;
        while ((texts = reader.readLine().split(";")) != null) {
            Contato contato = new Contato(texts[0], texts[1], texts[2]);
            gravarContato(contato);
        }
        reader.close();
    }

    public void finalize() {
        try {
            connection.close();

        } catch (SQLException exception) {
            exception.printStackTrace();
        }
    }

    /**
     * 
     * @param contato
     * @return novoContato
     * @throws SQLException
     */
    @Override
    public boolean gravarContato(Contato contato) throws SQLException {
        var sql = "SELECT 1 FROM Agenda WHERE Telefone = ?";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        preparedStatement.setString(1, contato.telefone);
        ResultSet resultSet = preparedStatement.executeQuery();
        var novoContato = !resultSet.next();
        resultSet.close();
        preparedStatement.close();

        sql = "UPDATE Agenda SET Nome = ?, Email = ? WHERE Telefone = ?";
        if (novoContato) sql = "INSERT INTO Agenda (Nome, Email, Telefone) VALUES (?, ?, ?)";

        preparedStatement = connection.prepareStatement(sql);
        preparedStatement.setString(1, contato.nome);
        preparedStatement.setString(2, contato.email);
        preparedStatement.setString(3, contato.telefone);
        preparedStatement.execute();
        preparedStatement.close();

        return novoContato;
    }

    @Override
    public void apagarContato(Contato contato) throws SQLException {
        var sql = "DELETE FROM Agenda WHERE Telefone = ?";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        preparedStatement.setString(1, contato.telefone);
        preparedStatement.executeUpdate();
        preparedStatement.close();
    }

    @Override
    public void listarContatos() throws SQLException {
        var sql = "SELECT * FROM Agenda";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        ResultSet resultSet = preparedStatement.executeQuery();
        System.out.println(String.format("\n%s; %s; %s", "Nome", "Telefone", "Email"));
        while (resultSet.next()) {
            System.out.println(String.format("%s; %s; %s",
                resultSet.getString("Nome"), 
                resultSet.getString("Telefone"), 
                resultSet.getString("Email")
            ));
        }
        resultSet.close();
        preparedStatement.close();
    }

    private void cadastrarContatos() throws IOException, SQLException {
        Contato contato = null;
        do {
            contato = cadastrarContato();
            listarContatos();
        } while (contato.nome.length() > 0);
    }

    private Contato cadastrarContato() throws IOException, SQLException {
        Contato contato = entrarContato();
        if (contato.nome.length() > 0) gravarContato(contato);
        return contato;
    }

    public static void main(String[] args) {
        try {
            var app = new App();
            app.cadastrarContatos();
            app.finalize();

        } catch (Exception exception) {
            exception.printStackTrace();
        }
    }
}