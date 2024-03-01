package net.cpbackend.dipendente;

import static org.junit.Assert.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.OK;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit4.SpringRunner;

import net.cpbackend.model.Dipendente;
import net.cpbackend.model.Stabilimento;
import net.cpbackend.model.Stanza;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class FindAllDipendentiTest {
	
	@Autowired
	private TestRestTemplate restTemplate;
	
	private Set<Dipendente> dipendenti;
	
	@BeforeEach
	void setUp() {
		Stabilimento stabilimento = new Stabilimento("test");
		stabilimento.setId(restTemplate.postForEntity("/officina/stabilimenti", stabilimento, Stabilimento.class).getBody().getId());
		
		if (stabilimento.getId() == null) throw new RuntimeException("Failed to initialize the stabilimento");
		
		Stanza stanza = new Stanza(stabilimento, "test", 120, 0);
		stanza.setId(restTemplate.postForEntity("/officina/stanze", stanza, Stanza.class).getBody().getId());
		
		if (stanza.getId() == null) throw new RuntimeException("Failed to initialize the stanza");
		
		List<Stanza> stanze = new ArrayList<>();
		stanze.add(stanza);
		
		dipendenti = new HashSet<>();
		
		for (int i = 0; i < 3; ++i) {
			Dipendente supervisore = new Dipendente("test", "test", "test", null, stanze);
			supervisore.setId(restTemplate.postForEntity("/officina/dipendenti", supervisore, Dipendente.class).getBody().getId());
			
			if (supervisore.getId() == null) throw new RuntimeException("Failed to initialize a dipendente supervisore");
			
			dipendenti.add(supervisore);
			
			Dipendente supervisionato = new Dipendente("test", "test", "test", supervisore, stanze);
			supervisionato.setId(restTemplate.postForEntity("/officina/dipendenti", supervisionato, Dipendente.class).getBody().getId());
			
			if (supervisionato.getId() == null) throw new RuntimeException("Failed to initialize a dipendente supervisionato");
			
			dipendenti.add(supervisionato);
		}
	}
	
	@AfterEach
	void tearDown() {		
		Iterator<Dipendente> iterator = dipendenti.iterator(); 
		
        while (iterator.hasNext()) { 
        	Dipendente dipendente = iterator.next();
        	
        	restTemplate.exchange("/officina/dipendenti/{id}", HttpMethod.DELETE,
    					null, Dipendente.class, dipendente.getId());
            
            if (!iterator.hasNext()) {
            	List<Stanza> stanze = (List<Stanza>) dipendente.getStanze();
            	
            	restTemplate.exchange("/officina/stanze/{id}", HttpMethod.DELETE,
        				null, Stanza.class, stanze.get(0).getId());
            	
            	restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.DELETE,
        				null, Stabilimento.class, stanze.get(0).getStabilimento().getId());
            }
        } 
	}
	
	@Test
	void findAll() {
		ResponseEntity<Set<Dipendente>> response = restTemplate.exchange("/officina/dipendenti", HttpMethod.GET,
				null, new ParameterizedTypeReference<Set<Dipendente>>() {
				});

		assertEquals(OK.value(), response.getStatusCode().value());
		
		assertTrue(response.getBody().containsAll(dipendenti));
	}
}
