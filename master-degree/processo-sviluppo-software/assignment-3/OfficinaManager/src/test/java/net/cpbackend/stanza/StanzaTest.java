package net.cpbackend.stanza;

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

import net.cpbackend.model.Stabilimento;
import net.cpbackend.model.Stanza;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class StanzaTest {

	@Autowired
	private TestRestTemplate restTemplate;
	
	private Stanza fixture;
	
	@BeforeEach
	void setUp() {
		Stabilimento stabilimento = new Stabilimento("test");
		stabilimento.setId(restTemplate.postForEntity("/officina/stabilimenti", stabilimento, Stabilimento.class).getBody().getId());
		
		if (stabilimento.getId() == null) throw new RuntimeException("Failed to initialize the stabilimento");
		
		fixture = new Stanza(stabilimento, "test", 50, 1);
		fixture.setId(restTemplate.postForEntity("/officina/stanze", fixture, Stanza.class).getBody().getId());
		
		if (fixture.getId() == null) throw new RuntimeException("Failed to initialize the fixture");
	}
	
	@AfterEach
	void tearDown() {
		restTemplate.exchange("/officina/stanze/{id}", HttpMethod.DELETE,
				null, Stanza.class, fixture.getId());
		
		restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.DELETE,
				null, Stabilimento.class, fixture.getStabilimento().getId());
	}

	@Test
	void findById() {
		ResponseEntity<Stanza> response = restTemplate.getForEntity("/officina/stanze/{id}",
				Stanza.class, fixture.getId());

		assertEquals(OK.value(), response.getStatusCode().value());
	}
	
	@Test
	void updateStanza() {
		fixture.setNome("test update");

		ResponseEntity<Stanza> response = restTemplate.exchange("/officina/stanze/{id}", HttpMethod.PUT,
				new HttpEntity<>(fixture), Stanza.class, fixture.getId());

		assertEquals(OK.value(), response.getStatusCode().value());
		assertEquals(response.getBody().getId(), fixture.getId());
		assertEquals(response.getBody().getNome(), fixture.getNome());
	}
}