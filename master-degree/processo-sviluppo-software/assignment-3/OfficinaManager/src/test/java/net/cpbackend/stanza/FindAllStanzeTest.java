package net.cpbackend.stanza;

import static org.junit.Assert.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.OK;

import java.util.HashSet;
import java.util.Iterator;
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

import net.cpbackend.model.Stabilimento;
import net.cpbackend.model.Stanza;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class FindAllStanzeTest {
	
	@Autowired
	private TestRestTemplate restTemplate;
	
	private Set<Stanza> stanze;
	
	@BeforeEach
	void setUp() {
		Stabilimento stabilimento = new Stabilimento("test");
		stabilimento.setId(restTemplate.postForEntity("/officina/stabilimenti", stabilimento, Stabilimento.class).getBody().getId());
		
		if (stabilimento.getId() == null) throw new RuntimeException("Failed to initialize the stabilimento");
		
		stanze = new HashSet<>();
		
		for (int i = 0; i < 3; ++i) {
			Stanza stanza = new Stanza(stabilimento, "test", 30, 4);
			stanza.setId(restTemplate.postForEntity("/officina/stanze", stanza, Stanza.class).getBody().getId());
			
			if (stanza.getId() == null) throw new RuntimeException("Failed to initialize a stanza");
			
			stanze.add(stanza);
		}
	}
	
	@AfterEach
	void tearDown() {		
		Iterator<Stanza> iterator = stanze.iterator(); 
		
        while (iterator.hasNext()) { 
        	Stanza stanza = iterator.next();
        	
            restTemplate.exchange("/officina/stanze/{id}", HttpMethod.DELETE,
					null, Stanza.class, stanza.getId());
            
            if (!iterator.hasNext()) {
            	restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.DELETE,
        				null, Stabilimento.class, stanza.getStabilimento().getId());
            }
        } 
	}
	
	@Test
	void findAll() {
		ResponseEntity<Set<Stanza>> response = restTemplate.exchange("/officina/stanze", HttpMethod.GET,
				null, new ParameterizedTypeReference<Set<Stanza>>() {
				});

		assertEquals(OK.value(), response.getStatusCode().value());
		
		assertTrue(response.getBody().containsAll(stanze));
	}
}
