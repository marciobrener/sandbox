package sandbox;

import java.io.IOException;
import java.io.File;

public interface Agenda {
    public boolean gravarContato(Contato contato) throws Exception;
    public void apagarContato(Contato contato) throws Exception;
    public Contato digitarContato() throws IOException;
    public void carregarContatos(File file) throws Exception;    
    public void listarContatos() throws Exception;
    public void apagarAgenda() throws Exception;
    public void criarAgenda() throws Exception;

}
