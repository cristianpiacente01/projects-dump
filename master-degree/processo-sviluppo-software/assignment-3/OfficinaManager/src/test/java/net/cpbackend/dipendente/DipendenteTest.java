package net.cpbackend.dipendente;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.OK;

import java.util.ArrayList;
import java.util.List;

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

import net.cpbackend.model.Dipendente;
import net.cpbackend.model.Stabilimento;
import net.cpbackend.model.Stanza;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class DipendenteTest {

	@Autowired
	private TestRestTemplate restTemplate;
	
	private Dipendente[] fixture; // {supervisore, supervisionato}
	
	@BeforeEach
	void setUp() {
		Stabilimento stabilimento = new Stabilimento("test");
		stabilimento.setId(restTemplate.postForEntity("/officina/stabilimenti", stabilimento, Stabilimento.class).getBody().getId());
		
		if (stabilimento.getId() == null) throw new RuntimeException("Failed to initialize the stabilimento");
		
		Stanza stanza = new Stanza(stabilimento, "test", 150, -2);
		stanza.setId(restTemplate.postForEntity("/officina/stanze", stanza, Stanza.class).getBody().getId());
		
		if (stanza.getId() == null) throw new RuntimeException("Failed to initialize the stanza");
		
		List<Stanza> stanze = new ArrayList<>();
		stanze.add(stanza);
		
		fixture = new Dipendente[2];
		
		fixture[0] = new Dipendente("test", "test", "test", null, stanze);
		fixture[0].setId(restTemplate.postForEntity("/officina/dipendenti", fixture[0], Dipendente.class).getBody().getId());
		
		if (fixture[0].getId() == null) throw new RuntimeException("Failed to initialize the dipendente supervisore");
		
		fixture[1] = new Dipendente("test", "test", "test", fixture[0], stanze);
		fixture[1].setId(restTemplate.postForEntity("/officina/dipendenti", fixture[1], Dipendente.class).getBody().getId());
		
		if (fixture[1].getId() == null) throw new RuntimeException("Failed to initialize the dipendente supervisionato");
	}
	
	@AfterEach
	void tearDown() {
		restTemplate.exchange("/officina/dipendenti/{id}", HttpMethod.DELETE,
				null, Dipendente.class, fixture[1].getId());
		
		restTemplate.exchange("/officina/dipendenti/{id}", HttpMethod.DELETE,
				null, Dipendente.class, fixture[0].getId());
		
		List<Stanza> stanze = (List<Stanza>) fixture[0].getStanze();
		
		restTemplate.exchange("/officina/stanze/{id}", HttpMethod.DELETE,
				null, Stanza.class, stanze.get(0).getId());
		
		restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.DELETE,
				null, Stabilimento.class, stanze.get(0).getStabilimento().getId());
	}

	@Test
	void findById() {
		assertEquals(OK.value(), restTemplate.getForEntity("/officina/dipendenti/{id}",
				Dipendente.class, fixture[0].getId()).getStatusCode().value());
		
		assertEquals(OK.value(), restTemplate.getForEntity("/officina/dipendenti/{id}",
				Dipendente.class, fixture[1].getId()).getStatusCode().value());
	}
	
	@Test
	void updateDipendente() {
		for (int i = 0; i <= 1; ++i) {
			fixture[i].setNome("test update");

			ResponseEntity<Dipendente> response = restTemplate.exchange("/officina/dipendenti/{id}", HttpMethod.PUT,
					new HttpEntity<>(fixture[i]), Dipendente.class, fixture[i].getId());

			assertEquals(OK.value(), response.getStatusCode().value());
			assertEquals(response.getBody().getId(), fixture[i].getId());
			assertEquals(response.getBody().getNome(), fixture[i].getNome());
		}
	}
}