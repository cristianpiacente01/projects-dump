package net.cpbackend.attrezzo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.OK;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
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
class AttrezzoTest {

	@Autowired
	private TestRestTemplate restTemplate;
	
	private Attrezzo[] fixture; // {motosega, trapano}
	
	@BeforeEach
	void setUp() {
		// create the stabilimento
		Stabilimento stabilimento = new Stabilimento("test");
		stabilimento.setId(restTemplate.postForEntity("/officina/stabilimenti", stabilimento, Stabilimento.class).getBody().getId());
		
		if (stabilimento.getId() == null) throw new RuntimeException("Failed to initialize the stabilimento");
		
		// create the stanza
		Stanza stanza = new Stanza(stabilimento, "test", 90, 5);
		stanza.setId(restTemplate.postForEntity("/officina/stanze", stanza, Stanza.class).getBody().getId());
		
		if (stanza.getId() == null) throw new RuntimeException("Failed to initialize the stanza");
		
		// create the attrezzi
		fixture = new Attrezzo[2];
		
		fixture[0] = new Motosega("test", "test", stanza, 100, "test");
		fixture[0].setId(restTemplate.postForEntity("/officina/attrezzi", fixture[0], Motosega.class).getBody().getId());
		
		if (fixture[0].getId() == null) throw new RuntimeException("Failed to initialize the motosega");
		
		fixture[1] = new Trapano("test", "test", stanza, 110, "test");
		fixture[1].setId(restTemplate.postForEntity("/officina/attrezzi", fixture[1], Trapano.class).getBody().getId());
		
		if (fixture[1].getId() == null) throw new RuntimeException("Failed to initialize the trapano");
	}
	
	@AfterEach
	void tearDown() {
		// delete the attrezzi
		restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.DELETE,
				null, Motosega.class, fixture[0].getId());
		
		restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.DELETE,
				null, Trapano.class, fixture[1].getId());
		
		// delete the stanza
		restTemplate.exchange("/officina/stanze/{id}", HttpMethod.DELETE,
				null, Stanza.class, fixture[0].getStanza().getId());
		
		// delete the stabilimento
		restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.DELETE,
				null, Stabilimento.class, fixture[0].getStanza().getStabilimento().getId());
	}

	@Test
	void findById() {
		// read the attrezzi
		assertEquals(OK.value(), restTemplate.getForEntity("/officina/attrezzi/{id}",
				Attrezzo.class, fixture[0].getId()).getStatusCode().value());
		
		assertEquals(OK.value(), restTemplate.getForEntity("/officina/attrezzi/{id}",
				Attrezzo.class, fixture[1].getId()).getStatusCode().value());
	}
	
	@Test
	void updateAttrezzo() {
		// update the modello of the attrezzi
		for (int i = 0; i <= 1; ++i) {
			fixture[i].setModello("test update");

			ResponseEntity<Attrezzo> response = restTemplate.exchange("/officina/attrezzi/{id}", HttpMethod.PUT,
					new HttpEntity<>(fixture[i]), Attrezzo.class, fixture[i].getId());

			assertEquals(OK.value(), response.getStatusCode().value());
			assertEquals(response.getBody().getId(), fixture[i].getId());
			assertEquals(response.getBody().getModello(), fixture[i].getModello());
		}
	}
}