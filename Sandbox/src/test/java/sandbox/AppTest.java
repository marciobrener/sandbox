package sandbox;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

/**
 * Unit test for simple App.
 */
public class AppTest extends TestCase
{
    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public AppTest(String testName) {
        super(testName);
    }

    private Contato stubContato() {
        Contato contato = new Contato();
        contato.nome = "teste";
        contato.telefone = "teste";
        contato.email = "teste";
        return contato;
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite() {
        return new TestSuite(AppTest.class);
    }

    public void teste() {
        var ok = false;
        try {
            new App().finalize();
            ok = true;
        } catch (Exception exception) {
            
        } finally {
            assertTrue("Execução Ok", ok);
        }
    }

    /**
     * Rigourous Test :-)
     */
    public void testApp() {
        assertTrue(true);
    }
}
