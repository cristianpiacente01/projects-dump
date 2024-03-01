package net.cpbackend.attrezzo;

import static org.junit.Assert.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.OK;

import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.stream.Collectors;

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

import net.cpbackend.model.Attrezzo;
import net.cpbackend.model.Motosega;
import net.cpbackend.model.Stabilimento;
import net.cpbackend.model.Stanza;
import net.cpbackend.model.Trapano;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class SearchFindAllAttrezziTest {
	
	// test findAll and search for both motosega and trapano
	
	@Autowired
	private TestRestTemplate restTemplate;
	
	private Set<Attrezzo> attrezzi;
	
	@BeforeEach
	void setUp() {
		// create the stabilimento
		Stabilimento stabilimento = new Stabilimento("test");
		stabilimento.setId(restTemplate.postForEntity("/officina/stabilimenti", stabilimento, Stabilimento.class).getBody().getId());
		
		if (stabilimento.getId() == null) throw new RuntimeException("Failed to initialize the stabilimento");
		
		// create the stanza
		Stanza stanza = new Stanza(stabilimento, "test", 10, -1);
		stanza.setId(restTemplate.postForEntity("/officina/stanze", stanza, Stanza.class).getBody().getId());
		
		if (stanza.getId() == null) throw new RuntimeException("Failed to initialize the stanza");
		
		attrezzi = new HashSet<>();
		
		// create a motosega and a trapano 3 times so the set will have 6 attrezzi
		for (int i = 0; i < 3; ++i) {
			Motosega motosega = new Motosega("test", "test", stanza, 70, "test");
			motosega.setId(restTemplate.postForEntity("/officina/attrezzi", motosega, Attrezzo.class).getBody().getId());
			
			if (motosega.getId() == null) throw new RuntimeException("Failed to initialize a motosega");
			
			attrezzi.add(motosega);
			
			Trapano trapano = new Trapano("test", "test", stanza, 75, "test");
			trapano.setId(restTemplate.postForEntity("/officina/attrezzi", trapano, Trapano.class).getBody().getId());
			
			if (trapano.getId() == null) throw new RuntimeException("Failed to initialize a trapano");
			
			attrezzi.add(trapano);
		}
	}
	
	@AfterEach
	void tearDown() {		
		Iterator<Attrezzo> iterator = attrezzi.iterator(); 
		
        while (iterator.hasNext()) { 
        	Attrezzo attrezzo = iterator.next();
        	
        	// delete the attrezzo
        	restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.DELETE,
    					null, Attrezzo.class, attrezzo.getId());
            
        	// if it was the last one
            if (!iterator.hasNext()) {
            	// delete the stanza
            	restTemplate.exchange("/officina/stanze/{id}", HttpMethod.DELETE,
        				null, Stanza.class, attrezzo.getStanza().getId());
            	
            	// delete the stabilimento
            	restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.DELETE,
        				null, Stabilimento.class, attrezzo.getStanza().getStabilimento().getId());
            }
        } 
	}
	
	@Test
	void search() {
		// create two subsets: one for the motoseghe and one for the trapani
		
		Set<Attrezzo> motoseghe = attrezzi.stream()
                .filter(attrezzo -> attrezzo.getTipo() == 'M')
                .collect(Collectors.toSet());
		
		Set<Attrezzo> trapani = attrezzi.stream()
                .filter(attrezzo -> attrezzo.getTipo() == 'T')
                .collect(Collectors.toSet());
		
		// perform two search operations because the passed type is different
		
		ResponseEntity<Set<Attrezzo>> responseM = restTemplate.exchange("/officina/attrezzi/search/{tipo}/{potenza}/{piano}", 
				HttpMethod.GET,
				null, new ParameterizedTypeReference<Set<Attrezzo>>() {},
				'M', 70, -1);

		assertEquals(OK.value(), responseM.getStatusCode().value());
		
		assertTrue(responseM.getBody().containsAll(motoseghe));
		
		ResponseEntity<Set<Attrezzo>> responseT = restTemplate.exchange("/officina/attrezzi/search/{tipo}/{potenza}/{piano}", 
				HttpMethod.GET,
				null, new ParameterizedTypeReference<Set<Attrezzo>>() {},
				'T', 75, -1);

		assertEquals(OK.value(), responseT.getStatusCode().value());
		
		assertTrue(responseT.getBody().containsAll(trapani));
	}
	
	@Test
	void findAll() {
		// find all attrezzi and check if the response contains the previously created attrezzi
		
		ResponseEntity<Set<Attrezzo>> response = restTemplate.exchange("/officina/attrezzi", HttpMethod.GET,
				null, new ParameterizedTypeReference<Set<Attrezzo>>() {
				});

		assertEquals(OK.value(), response.getStatusCode().value());
		
		assertTrue(response.getBody().containsAll(attrezzi));
	}
}
